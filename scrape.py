import requests
from bs4 import BeautifulSoup

index = requests.get('https://www.washingtonpost.com/news/post-politics/wp/2015/06/16/full-text-donald-trump-announces-a-presidential-bid/')
soup = BeautifulSoup(index.text, 'html.parser')
article = soup.find('article')
for p in article.findAll('p'):
    print('TRUMP: ' in p.text)
    print(p.text)

def parse_speech(url, text_body_tag='article'):
    index = requests.get(url)
    soup = BeautifulSoup(index.text, 'html.parser')
    article = soup.find(text_body_tag)
    
