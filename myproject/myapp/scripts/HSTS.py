import aiohttp
import asyncio
import re


async def check_hsts_and_print_result(url):
    result = await check_hsts_compatibility(url)
    return format_result(result)

async def check_hsts_compatibility(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as response:
                headers = response.headers
                hsts_header = headers.get('strict-transport-security')

                if not hsts_header:
                    return {'message': 'HSTS not Enabled. Site does not serve any HSTS headers.', 'compatible': False, 'hstsHeader': None}

                max_age_match = re.search(r'max-age=(\d+)', hsts_header)
                includes_subdomains = 'includeSubDomains' in hsts_header
                preload = 'preload' in hsts_header

                details = {
                    'HSTS Enabled': True,
                    'max-age': max_age_match.group(1) if max_age_match else 'N/A',
                    'includeSubDomains': includes_subdomains,
                    'preload': preload
                }

                if max_age_match and int(max_age_match.group(1)) >= 10886400 and includes_subdomains and preload:
                    return {'message': 'Site is compatible with the HSTS preload list!', 'compatible': True, 'hstsHeader': hsts_header, 'details': details}
                else:
                    return {'message': 'HSTS header does not include all subdomains.', 'compatible': False, 'hstsHeader': hsts_header, 'details': details}

    except Exception as e:
        return {'message': f'Error making request: {str(e)}', 'compatible': False, 'hstsHeader': None}

# Function to format the result into a string
def format_result(result):
    formatted_result = result['message']
    details = result.get('details')
    
    if details:
        formatted_result += "\nDetails:\n"
        for key, value in details.items():
            formatted_result += f"  - {key}: {value}\n"
    
    return formatted_result

# Function to take a URL and return the formatted result
async def get_hsts_info(url):
    return await check_hsts_and_print_result(url)


