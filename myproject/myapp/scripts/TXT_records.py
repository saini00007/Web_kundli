import dns.resolver
import tldextract
import asyncio

def extract_domain_name(url):
   
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def get_txt_records(domain):
    
    try:
        # Query DNS TXT records using dnspython
        answers = dns.resolver.resolve(domain, 'TXT')
        txt_records = {}
        
        for rdata in answers:
            for txt_string in rdata.strings:
                # Extract key-value pairs from TXT records if present
                parts = txt_string.decode().split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    txt_records[key] = value
        
        return txt_records
    except dns.resolver.NoAnswer:
        return "No TXT records found."
    except dns.resolver.NXDOMAIN:
        return "Domain does not exist."
    except Exception as e:
        return f"Error: {str(e)}"

async def main(url):
    
    domain = extract_domain_name(url)
    txt_records = get_txt_records(domain)
    
    if isinstance(txt_records, dict):
        result = ""
        for key, value in txt_records.items():
            result += f"{key} = {value}\n"
    else:
        result = txt_records
    
    return result


