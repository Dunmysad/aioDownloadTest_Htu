#!/usr/bin/env python3
import asyncio
import aiohttp
from lxml import etree

    
start_url = 'https://www.htu.edu.cn/9547/list.htm'

# 获取每一张图片的地址
def getImages():
    resp = requests.get(start_url).content.decode()
    html = etree.HTML(resp)
    urls = ['https://www.htu.edu.cn' + item for item in html.xpath('../html/body/div[3]/div/div/div[2]/div/div/ul/li/div/@href')] 
    return urls

async def aioDownload(url):
    name = url.rsplit("/", 1)[1]
    async with aiohttp.ClinetSession() as session:
        async with session.get(url).content.decode() as resp:
            html = etree.HTML(resp)
            image = 'https://www.htu.edu.cn' + html.xpath(../html/body/div[3]/div[1]/div/div[1]/img/src)
            with open(name, mode="wb") as f:
                f.write(await image.content.read())

async def main():
    tasks = getImages()
    for url in urls:
        tasks.append(aioDownload(url))
    await asyncio.wait(tasts)


if __name__ == '__main__':
    async.run(main())
