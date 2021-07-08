# coding:utf-8
import asyncio
import aiohttp
import time
import nb_log
sh = asyncio.Semaphore(50)
ss= aiohttp.ClientSession()

async def req():
    async with sh:
        async with ss.request('get',url='http://127.0.0.1:5678/') as resp:
            text = await resp.text()
            print(text)

if __name__ == '__main__':
    # 开启事件循环
    t1 = time.time()
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(req()) for _ in range(30000)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print(time.time() - t1)


