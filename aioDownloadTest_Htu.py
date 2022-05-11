#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import requests
import asyncio
import aiohttp
from lxml import etree
import os
import aiofiles
import time

fr_url = 'https://www.htu.edu.cn'
start_url = 'https://www.htu.edu.cn/9547/list.htm'
get_urls = []
images_urls = []

# 获取官网照片网页内所有单个照片网页的地址
def geturls(start_url):
    resp = requests.get(start_url).content.decode()
    html = etree.HTML(resp)
    urls = html.xpath('//*[@id="wp_news_w29"]/div/div/div/ul/li/div/@href')
    for url in urls:
        get_urls.append(f'{fr_url}{url}')

# 获取照片的下载地址
def getimagesurl(url):
    html = etree.HTML(requests.get(url).content.decode())
    images_url = html.xpath('../html/body/div[3]/div[1]/div/div[1]/img/@src')[0]
    images_urls.append(f'{fr_url}{images_url}')
    print(f'照片地址 {fr_url}{images_url} 解析完成')


async def aioDownload(url, session):
    name = url.split("-", 1)[-1]
    async with session.get(url, timeout=1000) as resp:
        # 使用aiofile写入文件
        async with aiofiles.open(f'./download/{name}', mode="wb") as f:
            print(f'开始下载图片 {name}')
            await f.write(await resp.content.read())
    print(name, '下载完成')

# 添加异步任务
async def test():
    async with aiohttp.ClientSession() as session:
        print('正在添加异步下载任务...')
        tasks = [asyncio.create_task(aioDownload(url, session)) for url in images_urls]
        await asyncio.wait(tasks)

if __name__ == '__main__':
    t1 = time.time()
    geturls(start_url)
    # 多线程获取照片下载路径
    with ThreadPoolExecutor(50) as t:
        for i in range(len(get_urls)):
            t.submit(getimagesurl, get_urls[i])
    # 处理创建文件夹问题
    try:
        os.mkdir('./download')
    except Exception as e:
        pass
    # 异步下载图片
    asyncio.run(test())
    t2 = time.time()
    print(f'一共下载图片{len(images_urls)}张 耗时 {t2-t1} s')
