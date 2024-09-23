import aiohttp
import asyncio

async def get_cookie_info(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            cookies = response.cookies
            cookie_info = {}
            for key, cookie in cookies.items():
                cookie_info[key] = {
                    "Domain": cookie.get("domain"),
                    "Path": cookie.get("path"),
                    "Expires": cookie.get("expires"),
                    "Secure": cookie.get("secure")
                }
            return cookie_info

async def handler(url):
    cookie_info = await get_cookie_info(url)
    
    if not cookie_info:
        return "No cookies found."
    else:
        # Format the cookies into a string result
        output = "Cookies:\n"
        for cookie_name, cookie_data in cookie_info.items():
            output += f"- {cookie_name}:\n"
            output += f"  Domain: {cookie_data['Domain'] or 'N/A'}\n"
            output += f"  Path: {cookie_data['Path'] or 'N/A'}\n"
            output += f"  Expires: {cookie_data['Expires'] or 'N/A'}\n"
            output += f"  Secure: {'Yes' if cookie_data['Secure'] else 'No'}\n"
            output += "\n"
        return output
    
