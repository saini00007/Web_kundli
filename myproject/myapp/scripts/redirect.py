import requests
import asyncio

def follow_redirects(url):
    try:
        # Initialize an empty list to store redirect URLs
        redirects = []
        
        # Perform a GET request and allow redirects
        response = requests.get(url, allow_redirects=True)
        
        # Append the original URL to the redirects list
        redirects.append(url)
        
        # Collect all the redirects
        for resp in response.history:
            redirects.append(resp.url)
        
        # Append the final URL (where the chain ends)
        redirects.append(response.url)
        
        # Remove duplicates
        redirects = list(dict.fromkeys(redirects))
        
        # Format the results into a string
        
        result = f"Site {len(redirects)} redirects when contacting host:\n"
        for redirect in redirects:
            result += f" ↳ {redirect}\n"
        
        return result

    except requests.RequestException as e:
        return f"An error occurred: {e}"

async def main(url):
   
    result = follow_redirects(url)
    return result


