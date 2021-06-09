import requests
from bs4 import BeautifulSoup

payload = {
    'email': 'luotaibin@gmail.com',
    'password': 'ltb518818lfan'
}

POST_LOGIN_URL = 'https://mbasic.facebook.com/login'
with requests.Session() as session:
    post = session.post(POST_LOGIN_URL, data=payload)
    page = session.get('https://m.facebook.com/browse/shares?id=1309059995969676')
content = BeautifulSoup(page.content, 'html.parser')
print(content)
names = content.find_all('span')
print('names -- >', names)
