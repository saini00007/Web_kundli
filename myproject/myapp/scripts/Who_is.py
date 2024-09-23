
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_whois_info(session, url):
    whois_url = f"https://www.whois.com/whois/{url}"
    async with session.get(whois_url) as response:
        html_content = await response.text()
        return html_content

async def get_whois_info(url):
    async with aiohttp.ClientSession() as session:
        html_content = await fetch_whois_info(session, url)
        soup = BeautifulSoup(html_content, 'html.parser')
        pre_tag = soup.find("pre", class_="df-raw")
        if pre_tag:
            whois_data = pre_tag.text.strip()
            return whois_data
        else:
            return None

def format_whois_info(whois_info):
    if whois_info:
        keys = ["Domain Name", "Registry Domain ID", "Registrar WHOIS Server", "Registrar URL", "Updated Date",
                "Creation Date", "Registrar Registration Expiration Date", "Registrar", "Registrar IANA ID",
                "Registrar Abuse Contact Email", "Registrar Abuse Contact Phone", "Reseller", "Domain Status",
                "Registry Registrant ID", "Registrant Name", "Registrant Organization", "Registrant Street",
                "Registrant City", "Registrant State/Province", "Registrant Postal Code", "Registrant Country",
                "Registrant Email", "Registry Admin ID", "Admin Name", "Admin Organization", "Admin Street",
                "Admin City", "Admin State/Province", "Admin Postal Code", "Admin Country", "Admin Phone",
                "Admin Fax", "Admin Email"]
    
        whois_dict = {}
        lines = whois_info.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                whois_dict[key.strip()] = value.strip()
        
        
        result = "\n"
        for key in keys:
            value = whois_dict.get(key, 'N/A')
            if value != 'N/A':
                result += f"{key}: {value}\n"
        return result
    else:
        return "WHOIS information not found for the provided URL."

async def main(url):
    
    whois_info = await get_whois_info(url)
    result = format_whois_info(whois_info)
    return result


