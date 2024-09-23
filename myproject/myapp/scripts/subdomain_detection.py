import aiohttp
import asyncio
from bs4 import BeautifulSoup
import tldextract

def extract_domain_name(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_subdomains(domain):
    subdomains = set()
    url = f"https://crt.sh/?dnsname={domain}&exclude=expired&group=none"
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 4:
                subdomain = cells[4].get_text().strip()
                if subdomain.endswith(domain):
                    subdomains.add(subdomain)
    return subdomains

def format_output(subdomains, domain):
    if subdomains:
        formatted = f"Found {len(subdomains)} subdomains for {domain}:\n"
        formatted += "\n".join(sorted(subdomains))
    else:
        formatted = f"No subdomains found for {domain}."
    return formatted

async def main(url):
    domain = extract_domain_name(url)
    subdomains = await get_subdomains(domain)
    result = format_output(subdomains, domain)
    return result 


