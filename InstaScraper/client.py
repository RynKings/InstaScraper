# -*- coding: utf-8 -*-
# Made with love by Ryns

import requests
import time
import json
import os
import pickle

from datetime import datetime

def loggedIn(func):
	def checkLogin(*args, **kwargs):
		if args[0].isLogin:
			return func(*args, **kwargs)
		else:
			print('You want to call the function, you must login to Instagram')
	return checkLogin

class InstaScraper:

	cookie_file = 'session.ryns'

	host		= 'https://www.instagram.com/'
	web			= host + 'web/'
	graphql		= host + 'graphql/query/'

	headers		= {
		'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36',
	}

	def __init__(self):
		self.isLogin = False
		self.tempUser = {}

	def getContent(self, url):
		if self.isLogin:
			return requests.get(url, headers=self.headers)
		else:
			return requests.get(url)

	def postContent(self, url, data=None, files=None):
		if self.isLogin:
			return requests.post(url, data=data, files=files, headers=self.headers)
		else:
			return requests.post(url, data=data, files=files)

	def getGraphqlContent(self, q_hash, variables):
		var = json.dumps(variables, separators=(',', ':'))
		url = f'{self.graphql}?query_hash={q_hash}&variables={var}'
		req = self.getContent(url).json()
		return req

	def getFeed(self, q_hash, variables, count):
		item_count = 0
		page = True
		result = []
		while page and item_count != count:
			req  = self.getGraphqlContent(q_hash, variables)
			data = req['data']['user']['edge_owner_to_timeline_media']
			page_info = data['page_info']
			for d in data['edges']:
				result.append(d['node'])
				item_count += 1
				if item_count == count:
					break

			page = page_info['has_next_page']
			variables['after'] = page_info['end_cursor']
		return result

	def login(self, username=None, password=None):
		if os.path.exists(self.cookie_file):
			cookie = pickle.load(open(self.cookie_file, 'rb'))
			if cookie['username'] == username:
				self.headers.update(cookie['headers'])
				self.isLogin = True
		else:
			req	    = requests.get(self.host)
			cookies = req.cookies.get_dict(domain='.instagram.com')
			headers = {
				'x-csrftoken': cookies['csrftoken'],
				'cookie': f'ig_did={cookies["ig_did"]}; mid={cookies["mid"]}; csrftoken={cookies["csrftoken"]}',
			}

			data	= {
				'username': username,
				'enc_password': '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), password)
			}

			req	 = requests.post(self.host + 'accounts/login/ajax/', data=data, headers=headers)
			if req.status_code != 200:
				raise Exception('Authenticanion Failure!!')

			cookies = req.cookies.get_dict(domain='.instagram.com')
			if 'sessionid' not in cookies or 'csrftoken' not in cookies:
				raise Exception('Authenticanion Failure!!')

			self.headers.update({
				'x-csrftoken': cookies['csrftoken'],
				'cookie': f"csrftoken={cookies['csrftoken']};sessionid={cookies['sessionid']}",
			})
			self.isLogin = True
			session = open(self.cookie_file, 'wb')
			sesdata = {
				'username': username,
				'headers': self.headers
			}
			pickle.dump(sesdata, session)

	def getUserId(self, username):
		if username in self.tempUser:
			userid = self.tempUser[username]
		else:
			userid = self.getProfile(username)['id']
			self.tempUser[username] = userid
		return userid

	def getProfile(self, username):
		url = self.host + username + '/?__a=1'
		req = self.getContent(url).json()['graphql']['user']
		res = {
			'id': req['id'],
			'username': req['username'],
			'full_name': req['full_name'],
			'profile_pic_url': req['profile_pic_url'],
			'profile_pic_url_hd': req['profile_pic_url_hd'],
			'biography': req['biography'],
			'external_url': req['external_url'],
			'followers_count': req['edge_followed_by']['count'],
			'followed_count': req['edge_follow']['count'],
			'is_bussiness': req['is_business_account'],
			'is_private': req['is_private'],
			'is_verified': req['is_verified'],
			'igtv_count': req['edge_felix_video_timeline']['count'],
			'media_count': req['edge_owner_to_timeline_media']['count']
		}
		return res

	def getPost(self, username, count=10):
		userid = self.getUserId(username)
		variables = {'id': userid, 'first': count}
		data = self.getFeed('472f257a40c653c64c666ce877d59d2b', variables, count)
		return data

	@loggedIn
	def getStory(self, username):
		userid = self.getUserId(username)
		variables = {"reel_ids":[userid], "precomposed_overlay":False,"show_story_viewer_list":True,"story_viewer_fetch_count":50,"story_viewer_cursor":"","stories_video_dash_manifest":False}
		data = self.getGraphqlContent('5ec1d322b38839230f8e256e1f638d5f', variables)
		data = data['data']['reels_media']
		if data:
			return data[0]['items']
		return data

if __name__ == '__main__':
	i = InstaScraper()
	i.login('USERNAME', 'PASSWORD')
	story = i.getStory('instagram')
	print(story)