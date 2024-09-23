import aiohttp
import asyncio
from urllib.parse import urlparse
import socket
import asyncio

async def get_domain_from_url(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain

async def get_ip_location(ip):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://ipapi.co/{ip}/json/") as response:
            data = await response.json()
            return data

def format_location_details(loc):
    if not loc:
        return "No Data Found...."
    
    keys = [
        'ip', 'version', 'City', 'Region', 'Country Code', 'Country', 'Continent Code',
        'postal', 'Latitude', 'Longitude', 'Timezone', 'UTC Offset', 'Country Calling Code',
        'Currency', 'Currency Name', 'Languages', 'ASN'
    ]
    
    
    formatted_result = "\n"
    
    for key in keys:
        value = loc.get(key.lower().replace(' ', '_'), 'N/A')
        formatted_result += f"{key}: {value}\n"
    
    return formatted_result

async def main(url):
    domain = await get_domain_from_url(url)
    ip = socket.gethostbyname(domain)
    loc = await get_ip_location(ip)
    result = format_location_details(loc)
    return result


