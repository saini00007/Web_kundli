import aiohttp
import asyncio

async def fetch_dnssec_records(domain, dns_type):
    url = f"https://dns.google/resolve?name={domain}&type={dns_type}"
    headers = {'Accept': 'application/dns-json'}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return f"Failed to fetch {dns_type} record: {response.status}"
                
                dns_response = await response.json()
                
                # Parse response for DNSSEC details
                is_found = bool(dns_response.get('Answer'))
                flags = dns_response.get('AD', False)
                
                return {
                    'is_found': is_found,
                    'flags': flags,
                    'answer': dns_response.get('Answer', [])
                }
    except Exception as e:
        return f"Error fetching {dns_type} record: {str(e)}"

async def get_dnssec_info(domain):
    dns_types = ['DNSKEY', 'DS', 'RRSIG']
    records = {}
    
    # Fetch DNSSEC records for the specified types
    tasks = [fetch_dnssec_records(domain, dns_type) for dns_type in dns_types]
    results = await asyncio.gather(*tasks)
    
    # Format the results
    result = ""
    for dns_type, record in zip(dns_types, results):
        if isinstance(record, str):
            result += "Not Found" # If there was an error, append the error message
        else:
            result += f"DNSSEC Record: {dns_type}\n"
            result += f"Present? {'Yes' if record['is_found'] else 'No'}\n"
            result += f"Authentic Data (AD) Flag: {'Yes' if record['flags'] else 'No'}\n"
            result += "\n"
    
    return result

