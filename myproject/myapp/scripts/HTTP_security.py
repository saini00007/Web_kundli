import requests
import asyncio


def check_headers(url, headers_to_check):
    try:
        response = requests.get(url)
        response_headers = response.headers
        
        result = ""

        for header in headers_to_check:
            if header in response_headers:
                result += f"[+] {header:<30}: YES\n"
            else:
                result += f"[-] {header:<30}: NO\n"
        return result

    except requests.exceptions.RequestException as e:
        return f"Error occurred during the request: {e}"

# Main function to be called with a URL
async def main(url):
    headers_to_check = [
        "strict-transport-security",
        "x-frame-options",
        "x-content-type-options",
        "x-xss-protection",
        "content-security-policy"
    ]
    return check_headers(url, headers_to_check)


