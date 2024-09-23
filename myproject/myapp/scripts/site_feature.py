import aiohttp
import re
import asyncio

# Asynchronous function to check if the feature exists in the HTML content
async def check_feature(session, url, feature):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                # Check for the presence of the feature using regex
                if re.search(feature + r'[^a-zA-Z0-9_-]', html_content, re.IGNORECASE):
                    return 'Live'
                else:
                    return 'Dead'
            else:
                return 'Error: Unable to fetch URL'
    except Exception as e:
        return f'Error: {str(e)}'

# Main handler to fetch and check all features
async def check_site_features(url):
    features = {
        'ssl': 'ssl',
        'javascript': 'javascript-library1|javascript',
        'framework': 'framework1',
        'us-hosting': 'us-hosting3',
        'cloud-hosting': 'cloud-hosting2',
        'cloud-paas': 'cloud-paas3',
        'server-location': 'server-location1',
        'application-performance': 'application-performance1',
        'audience-measurement': 'audience-measurement2',
        'dmarc': 'dmarc1'
    }

    
   

    async with aiohttp.ClientSession() as session:
        tasks = [check_feature(session, url, value) for value in features.values()]
        feature_results = await asyncio.gather(*tasks)
    result = "\n"
    # Formatting the result for each feature
    for key, feature_result in zip(features.keys(), feature_results):
    
        result += f"{key} : {feature_result} \n"

    return result

# Example usage to fetch and print results
