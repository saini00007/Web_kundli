import aiohttp
import asyncio
import tldextract

API_BASE_URL = "https://tranco-list.eu/api/"

def extract_domain(url):
    extracted = tldextract.extract(url)
    return extracted.domain + '.' + extracted.suffix

async def get_global_rank(url):
    try:
        async with aiohttp.ClientSession() as session:
            endpoint = f"{API_BASE_URL}/ranks/domain/{url}"
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    ranks = data.get("ranks", [])
                    
                    if ranks:
                        # Find the latest date in the ranks data
                        latest_rank = max(ranks, key=lambda x: x["date"])
                        latest_date = latest_rank["date"]
                        latest_rank_value = latest_rank["rank"]
                        
                        return (
                            f"Domain : {url}\n"
                            f"Date : {latest_date}\n"
                            f"Global Rank : {latest_rank_value}\n"
                        )
                    else:
                        return {"Error": "No rank data found for the given domain."}
                else:
                    return {"Error": "No rank found for the given domain."}
    except Exception as e:
        return {"Error": str(e)}

async def main(url):
    
    domain = extract_domain(url)
    result = await get_global_rank(domain)
    return result


