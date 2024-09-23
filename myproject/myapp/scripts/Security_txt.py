import requests
from urllib.parse import urlparse, urljoin
import asyncio

SECURITY_TXT_PATHS = [
    '/security.txt',
    '/.well-known/security.txt',
]

def parse_result(result):
    output = {}
    counts = {}
    lines = result.split('\n')
    for line in lines:
        if not line.startswith("#") and not line.startswith("-----") and line.strip() != '':
            key_value = line.split(':', 1)
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                if key in output:
                    counts[key] = counts.get(key, 0) + 1
                    key += str(counts[key])
                output[key] = value
    return output

def is_pgp_signed(result):
    return '-----BEGIN PGP SIGNED MESSAGE-----' in result

def handler(url_param):
    try:
        url = urlparse(url_param) if '://' in url_param else urlparse('https://' + url_param)
    except Exception as e:
        raise ValueError('Invalid URL or URL is not responding to this query.')

    base_url = url._replace(path='').geturl()

    for path in SECURITY_TXT_PATHS:
        try:
            result = fetch_security_txt(base_url, path)
            if result and '<html' in result:
                return {'isPresent': False}
            if result:
                return {
                    'isPresent': True,
                    'foundIn': path,
                    'content': result,
                    'isPgpSigned': is_pgp_signed(result),
                    'fields': parse_result(result),
                }
        except Exception as e:
            raise Exception(str(e))

    return {'isPresent': False}

def fetch_security_txt(base_url, path):
    url = urljoin(base_url, path)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def format_result(result):
    output = []
    

    if result['isPresent']:
        
        output.append(f"\nSecurity.txt{' ' * 5}--> present")
        output.append(f"File Location{' ' * 5}: {result['foundIn']}")
        output.append(f"PGP Signed{' ' * 5}: {'Yes' if result['isPgpSigned'] else 'No'}")
        for key, value in result['fields'].items():
            output.append(f"{key:<20} : {value}")
    else:
        output.append(f"\nSecurity.txt{' ' * 5}--> not present")

    return "\n".join(output)

async def main(url):
        result = handler(url)
        formatted_output = format_result(result)
        return(formatted_output)