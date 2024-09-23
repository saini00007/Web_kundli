import asyncio
import socket
from urllib.parse import urlparse

async def resolve_dns(url):
    try:
        # Extract domain from URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Resolve IPv4 addresses
        addresses = socket.gethostbyname_ex(domain)[-1]
        
        results = []
        for address in addresses:
            # Reverse DNS lookup
            try:
                hostname = socket.gethostbyaddr(address)[0]
            except socket.herror:
                hostname = None
            
            # Since we removed the session and DoH check, we just add the address and hostname.
            results.append({
                'address': address,
                'hostname': hostname,
                  # Placeholder for DoH support
            })

        return {
            'domain': domain,
            'dns': results
        }
    except Exception as e:
        raise Exception(f"An error occurred while resolving DNS: {str(e)}")

def format_dns_result(result):
    formatted_output = ""
    n = 1
    for item in result["dns"]:
        formatted_output += f"DNS Server No.{n}\n"
        
        if "address" in item:
            formatted_output += f"{'IP Address':<20} : {item['address']}\n"
        if "hostname" in item:
            formatted_output += f"{'Hostname':<20} : {item['hostname']}\n"
        if "dohDirectSupports" in item:
            formatted_output += f"{'DoH Support':<20} : {item['dohDirectSupports']}\n"
        
        formatted_output += "\n"
        n += 1
    
    return formatted_output

async def get_dns_server(url):
    dns_data = await resolve_dns(url)
    if dns_data:
        return format_dns_result(dns_data)
    return "Failed to fetch DNS records."


