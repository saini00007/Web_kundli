import aiohttp
import asyncio

async def fetch_headers(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as response:
                headers = response.headers
                return headers
    except Exception as e:
        return {'error': str(e)}

def format_text_headers(headers):
    output = ""  # Initialize output string
    if headers:
        for key, value in headers.items():
            output += f"{key}: {value}\n"  # Concatenate headers with newline
    else:
        output += "Failed to retrieve headers for the provided URL.\n"
    return output

async def main(url):
    headers = await fetch_headers(url)
    text_result = format_text_headers(headers)
    return text_result


