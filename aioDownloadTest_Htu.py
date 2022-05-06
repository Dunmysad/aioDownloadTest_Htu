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

# 获取官网照片网页内所有单个照片网页的地址
def geturls(start_url):
    resp = requests.get(start_url).content.decode()
    html = etree.HTML(resp)
    urls = html.xpath('../html/body/div[3]/div/div/div[2]/div/div/ul/li/div/@href')
    for url in urls:
        get_urls.append(f'{fr_url}{url}')

# 获取照片的下载地址
def getimagesurl(url):
    html = etree.HTML(requests.get(url).content.decode())
    images_url = html.xpath('../html/body/div[3]/div[1]/div/div[1]/img/@src')[0]
    images_urls.append(f'{fr_url}{images_url}')
    print(f'照片地址 {fr_url}{images_url} 解析完成')


async def aioDownload(url):
    name = url.split("-", 1)[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=1000) as resp:
            # 使用aiofile写入文件
            async with AIOFile(f'./download/{name}', mode="wb") as f:
                writer = Writer(f)
                print(f'开始下载图片 {name}')
                await writer(await resp.content.read())
    print(name, '下载完成')

# 添加异步任务
async def test():
    print('正在添加异步下载任务...')
    tasks = [asyncio.create_task(aioDownload(url)) for url in images_urls]
    await asyncio.wait(tasks)

if __name__ == '__main__':
    t1 = time.time()
    geturls(Url)
    # 多线程获取照片下载路径
    with ThreadPoolExecutor(50) as t:
        for i in range(len(get_urls)):
            t.submit(getimagesurl, get_urls[i])
    print(f'图片一共有 {len(images_urls)} 张')
    # 处理创建文件夹问题
    try:
        os.mkdir('./download')
    except Exception as e:
        pass
    # 异步下载图片
    asyncio.run(test())
    t2 = time.time()
    print(f'耗时 {t2-t1} s')
