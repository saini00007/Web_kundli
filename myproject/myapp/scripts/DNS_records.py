import aiohttp
import asyncio
import json

async def fetch_dns_records(domain):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.whoisfreaks.com/v2.0/dns/live?apiKey=bac036a63ee74c3698be8bc85fbefdef&domainName={domain}&type=all"
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None

def format_dns_output(json_data):
    formatted_output = ""
    try:
        data = json.loads(json_data)
        for record in data['dnsRecords']:
            formatted_output += f"DNS Type: {record['dnsType']}\n"
            formatted_output += f"TTL: {record['ttl']}\n"
            formatted_output += f"Raw Text: {record['rawText']}\n"
            formatted_output += f"RRset Type: {record['rRsetType']}\n"
            formatted_output += f"Address: {record.get('address', 'N/A')}\n\n"
    except json.JSONDecodeError:
        formatted_output = "Unable to get DNS records"
    return formatted_output

async def get_dns_records(domain):
    dns_data = await fetch_dns_records(domain)
    if dns_data:
        return format_dns_output(dns_data)
    return "Failed to fetch DNS records."
