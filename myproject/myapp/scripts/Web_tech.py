import aiohttp
import asyncio


async def get_http_headers(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True) as response:
                if response.status == 200:
                    return dict(response.headers)
                return None
    except aiohttp.ClientError as e:
        return None

def identify_web_technologies(http_headers):
    if not http_headers:
        return None

    technologies = (
        f"Server: {http_headers.get('Server', 'Unknown')}\n"
        f"X-Powered-By: {http_headers.get('X-Powered-By', 'Not specified')}\n"
        f"X-AspNet-Version: {http_headers.get('X-AspNet-Version', 'Not specified')}\n"
    )


    return technologies

async def main(url):
    
    http_headers = await get_http_headers(url)
    if http_headers:
        web_technologies = identify_web_technologies(http_headers)
        return web_technologies
    else:
        return "Unable to retrieve HTTP headers."


