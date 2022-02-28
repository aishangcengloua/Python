import _aiohttp
import asyncio

async def fetch(session, url) :
    print('发送请求', url)
    async with session.get(url, verify_ssl = False) as response :
        content = await response.content.read()
        file_name = url.split("-")[-1]
        with open(file_name, 'wb') as fp :
            fp.write(content)
        print('下载完成', url)

async def main() :
    async with _aiohttp.ClientSession() as session :
        url_list = [
            'https://pic.netbian.com/uploads/allimg/220221/224056-16454544561986.jpg',
            'https://pic.netbian.com/uploads/allimg/220219/000043-1645200043ee4e.jpg',
            'https://pic.netbian.com/uploads/allimg/220218/003619-16451157794080.jpg',
        ]
        tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]
        print(tasks)
        await asyncio.wait(tasks)

if __name__ == "__main__" :
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())