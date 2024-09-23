import aiohttp
import asyncio
import base64
import tldextract


# Replace with your VirusTotal API key
VT_API_KEY = '57e3de8428a9e14885e553719f4800e738d2150b1058e51ee9b1dc0b9b0a044d'

def url_to_base64(url):
    """Encode URL to a format suitable for VirusTotal API."""
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

def extract_domain(url):
    """Extract domain from URL using tldextract."""
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

async def check_virus_total(url):
    """Check URL against VirusTotal and return status."""
    headers = {
        'x-apikey': VT_API_KEY
    }
    encoded_url = url_to_base64(url)
    analysis_url = f"https://www.virustotal.com/api/v3/urls/{encoded_url}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(analysis_url, headers=headers) as response:
                response.raise_for_status()  # Raises an HTTPError if the response was an HTTP error
                analysis_data = await response.json()

                if 'data' in analysis_data:
                    positives = analysis_data['data']['attributes']['last_analysis_stats']['malicious']
                    if positives > 0:
                        return False, analysis_data
                    return True, analysis_data
                else:
                    return False, analysis_data
    except aiohttp.ClientResponseError as http_err:
        return False, {}
    except Exception as err:
        return False, {}

async def get_security_status(url):
    """Get overall security status of the URL."""
    vt_safe, vt_details = await check_virus_total(url)
    
     
    if vt_safe:
        status = "Webpage is ✅ Safe "
    else:
        status=+ "Webpage is not ❌ Not Safe "
    
    
    return status

async def main(url):
   
    domain = extract_domain(url)
    status = await get_security_status(domain)
    return status

