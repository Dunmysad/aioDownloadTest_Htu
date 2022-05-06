#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import requests
import asyncio
import aiohttp
from lxml import etree
import os
from aiofile import AIOFile, Writer, Reader
import time

fr_url = 'https://www.htu.edu.cn'
Url = 'https://www.htu.edu.cn/9547/list.htm'
get_urls = []
images_urls = []

def geturls(start_url):
    resp = requests.get(start_url).content.decode()
    html = etree.HTML(resp)
    urls = html.xpath('../html/body/div[3]/div/div/div[2]/div/div/ul/li/div/@href')
    for url in urls:
        get_urls.append(f'{fr_url}{url}')
    print(get_urls)

def getimagesurl(url):
    html = etree.HTML(requests.get(url).content.decode())
    images_url = html.xpath('../html/body/div[3]/div[1]/div/div[1]/img/@src')[0]
    images_urls.append(f'{fr_url}{images_url}')
    print(f'{fr_url}{images_url}')


async def aioDownload(url):
    name = url.split("-", 1)[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=1000) as resp:
            async with AIOFile(f'./download/{name}', mode="wb") as f:
                writer = Writer(f)
                await writer(await resp.content.read())
    print(name, '下载完成')

async def test():
    tasks = [asyncio.create_task(aioDownload(url)) for url in images_urls]
    await asyncio.wait(tasks)

if __name__ == '__main__':
    t1 = time.time()
    geturls(Url)
    with ThreadPoolExecutor(50) as t:
        for i in range(len(get_urls)):
            t.submit(getimagesurl, get_urls[i])
    print(images_urls)
    print(len(images_urls))
    try:
        os.mkdir('./download')
    except Exception as e:
        pass
    asyncio.run(test())
    t2 = time.time()
    print(t2-t1)
