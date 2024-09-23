import aiohttp
import asyncio
import tldextract

# Extract domain name from URL
def extract_domain_name(url):
    extracted = tldextract.extract(url)
    domain_name = f"{extracted.domain}.{extracted.suffix}"
    return domain_name

# Asynchronous function to fetch DNS records
async def fetch_dns_record(domain, record_type):
    url = f"https://dns.google/resolve?name={domain}&type={record_type}"
    headers = {'Accept': 'application/dns-json'}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return "Record not found."
                
                dns_response = await response.json()
                
                if 'Answer' in dns_response:
                    return '\n'.join([answer['data'] for answer in dns_response['Answer']])
                else:
                    return "Record not found."
    except Exception as e:
        return f"Error fetching {record_type} record: {str(e)}"

# Main handler to fetch all records
async def fetch_email_configurations(url):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    
    # Extract relevant domain records
    spf_record = await fetch_dns_record(domain, 'TXT')
    dkim_record = await fetch_dns_record(f'_domainkey.{domain}', 'TXT')
    dmarc_record = await fetch_dns_record(f'_dmarc.{domain}', 'TXT')
    bimi_record = await fetch_dns_record(f'_bimi.{domain}', 'TXT')
    
    # Formatting the result string
    
    # SPF Record
    result = f"SPF Record:\n"
    if spf_record != "Record not found.":
        result += f"  Status: Found\n  Content: {spf_record}\n"
    else:
        result += "  Status: Not found\n"
    
    # DKIM Record
    result += f"\nDKIM Record:\n"
    if dkim_record != "Record not found.":
        result += f"  Status: Found\n  Content: {dkim_record}\n"
    else:
        result += "  Status: Not found\n"
    
    # DMARC Record
    result += f"\nDMARC Record:\n"
    if dmarc_record != "Record not found.":
        result += f"  Status: Found\n  Content: {dmarc_record}\n"
    else:
        result += "  Status: Not found\n"
    
    # BIMI Record
    result += f"\nBIMI Record:\n"
    if bimi_record != "Record not found.":
        result += f"  Status: Found\n  Content: {bimi_record}\n"
    else:
        result += "  Status: Not found\n"
    
    return result

# Example function to fetch configurations and print the output

