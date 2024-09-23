import asyncio
import ssl
import socket


def extract_hostname(url):
    """Extract the hostname from the URL."""
    return url.split('/')[2]

async def get_cipher_suites_info(url):
    """Retrieve cipher suites and SSL/TLS information."""
    hostname = extract_hostname(url)
    
    loop = asyncio.get_event_loop()
    context = ssl.create_default_context()

    try:
        # Create a connection and wrap it with SSL/TLS
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cipher_suites = ssock.cipher()
                ssl_info = ssock.getpeercert()
                
                # Extract relevant SSL/TLS information
                key_exchange = ssl_info.get('keyExchange', 'Unknown')
                return (
                     f"Cipher Name: {cipher_suites[0]}\n"
                     f"TLS Version: {cipher_suites[1]}\n"
                     f"Key Exchange Protocol: {key_exchange}\n"
                     f"Public Key Algorithm: {ssl_info.get('pubkeyType', 'Unknown')}\n"
                     f"Signature Algorithm: {ssl_info.get('signatureAlgorithm', 'Unknown')}\n"
                     f"Session Ticket Supported: {ssl_info.get('session_ticket_supported', False)}\n"
                     f"OCSP Stapling Supported: {ssl_info.get('ocsp_response', False)}\n"
                     f"Perfect Forward Secrecy: {cipher_suites[2]}\n"
                     f"Elliptic Curves Supported: {ssl_info.get('ecdh_nid', 'No')}\n"
                )
    except Exception as e:
        return {"Error": str(e)}

async def main(url):
    
    cipher_info = await get_cipher_suites_info(url)
    return cipher_info

