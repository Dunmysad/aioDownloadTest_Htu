import re
import requests
from lxml import etree

url = 'https://www.htu.edu.cn'

def geturl(url):
    print(requests.get(url).content.decode())
    resp = re.compile(r'<a href="(?P<next_url>.*?)">', re.S)
    result = resp.finditer(requests.get(url).content.decode())
    for i in result:
        print(i.group())

if __name__ == '__main__':
    geturl(url)