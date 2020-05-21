*Instagram Scrapper*

## Installation
```cmd
git clone https://github.com/rynkings/InstaScraper
cd InstaScrapper
python setup.py install
```

## Example usage without login
```python
from InstaScraper import *
client = InstaScraper()
user_posts = client.getPost('ray.en_king', limit=5)
print(user_posts)
```

## Example usage with login
```python
from InstaScraper import *
client = InstaScraper()
client.login('USERNAME','PASSWORD')
user_strorys = client.getStory('instagram')
print(user_strorys)
```

## Author
Ryns / [@ray.en_king](https://www.instagram.com/ray.en_king)
