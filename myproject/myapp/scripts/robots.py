import aiohttp
from urllib.parse import urljoin
import asyncio

async def get_robots_txt(url):
    # Get the base URL
    base_url = urljoin(url, "/")

    # Fetch the robots.txt file
    robots_url = urljoin(base_url, "robots.txt")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(robots_url) as response:
            # Initialize result variable
            result = ""

            if response.status != 200:
                result = f"Failed to fetch robots.txt: {response.status}"
                
                return result

            # Parse robots.txt and extract rules
            lines = (await response.text()).splitlines()
            user_agent = ""
            crawl_rules = []
            for line in lines:
                if line.lower().startswith("user-agent:"):
                    user_agent = line.split(":")[1].strip()
                elif line.lower().startswith(("allow:", "disallow:")):
                    rule = line.split(":")[1].strip()
                    crawl_rules.append((user_agent, rule))

            # Format the result as a string
            if not crawl_rules:
                result = "No crawl rules found."
                
            else:
                
                for user_agent, rule in crawl_rules:
                    result += f"User-Agent: {user_agent}\n"
                    if "allow" in rule.lower():
                        result += f"Allow: {rule}\n"
                    else:
                        result += f"Disallow: {rule}\n"
                    result += "\n"
            
            return result
