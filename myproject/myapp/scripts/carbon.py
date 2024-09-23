import aiohttp
import asyncio

async def get_html_size(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                html_content = await response.text()
                size_in_bytes = len(html_content.encode('utf-8'))
                return size_in_bytes
    except aiohttp.ClientResponseError as e:
        if e.status == 403:
            raise ValueError("Forbidden: You don't have permission to access this resource.")
        else:
            raise ValueError(f"Error fetching HTML size: {e}")

async def get_carbon_data(size_in_bytes):
    try:
        api_url = f"https://api.websitecarbon.com/data?bytes={size_in_bytes}&green=0"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise ValueError(f"Error fetching carbon data: {e}")

async def handler(url):
    try:
        size_in_bytes = await get_html_size(url)
        carbon_data = await get_carbon_data(size_in_bytes)
        
        if 'statistics' not in carbon_data or (carbon_data['statistics']['adjustedBytes'] == 0 and carbon_data['statistics']['energy'] == 0):
            return {"skipped": "Not enough info to get carbon data"}
        
        carbon_data['scanUrl'] = url
        return carbon_data
    except Exception as e:
        return {"error": str(e)}

async def format_carbon_data(data):
    output = ""
    if 'skipped' in data:
        output += f"Skipped: {data['skipped']}\n"
        return output

    if 'error' in data:
        output += f"Error: {data['error']}\n"
        return output

    output += f"  - HTML Initial Size: {data['statistics']['adjustedBytes']} bytes\n"
    output += f"  - CO2 for Initial Load: {data['statistics']['co2']['grid']['grams']} grams\n"
    output += f"  - Energy Usage for Load: {data['statistics']['energy']:.4f} KWg\n"
    output += f"  - CO2 Emitted: {data['statistics']['co2']['renewable']['grams']} grams\n"
    
    return output


async def run_carbon_footprint(url):
    result = await handler(url)
    output = await format_carbon_data(result)
    return output
