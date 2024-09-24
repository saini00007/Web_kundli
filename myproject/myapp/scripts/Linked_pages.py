import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import asyncio

def handler(url):
    try:
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        internal_links_map = {}
        external_links_map = {}

        # Get all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)

            # Increment occurrence count
            if absolute_url.startswith(url):
                internal_links_map[absolute_url] = internal_links_map.get(absolute_url, 0) + 1
            elif href.startswith(('http://', 'https://')):
                external_links_map[absolute_url] = external_links_map.get(absolute_url, 0) + 1

        
        # Sort by most occurrences
        internal_links = sorted(internal_links_map.keys(), key=lambda k: internal_links_map[k], reverse=True)
        external_links = sorted(external_links_map.keys(), key=lambda k: external_links_map[k], reverse=True)

        # If there were no links, return a message
        if not internal_links and not external_links:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'skipped': 'No internal or external links found.'
                })
            }

        # Extract the part of the internal links that comes after the provided URL
        base_url_len = len(url)
        internal_links = [link[base_url_len:] for link in internal_links]

        return {'internal': internal_links, 'external': external_links}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {'error': str(e)}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}

def beautify_output(result):
    formatted_result = ""
    
    if 'error' in result:
        return f"Error: {result['error']}\n"

    if 'internal' in result:
        internal_links = result['internal']
        formatted_result += "Internal Links:\n"
        if internal_links:
            for link in internal_links:
                formatted_result += f"  - {link}\n"
        else:
            formatted_result += "  No internal links found.\n"
    
    if 'external' in result:
        external_links = result['external']
        formatted_result += "\nExternal Links:\n"
        if external_links:
            for link in external_links:
                formatted_result += f"  - {link}\n"
        else:
            formatted_result += "  No external links found.\n"

    return formatted_result


async def main(url):
    result = handler(url)
    output = beautify_output(result)
    # Return or process the formatted output as needed
    return output


