import ssl
import socket
from OpenSSL import crypto
from datetime import datetime
import asyncio

def get_ssl_certificate_info(url):
    # Extract hostname from the URL
    hostname = url.split('://')[1].split('/')[0]
    
    # Create a context for SSL
    context = ssl.create_default_context()
    
    try:
        # Connect to the server and get the certificate
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                certificate = ssock.getpeercert()
                if certificate is None:
                    return "Failed to retrieve SSL certificate."
                
                # Convert the certificate to an OpenSSL X509 object
                x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(ssock.getpeercert(True)))
                
                result = (
                    f"Subject: {x509.get_subject().CN}\n"
                    f"Issuer: {x509.get_issuer().CN}\n"
                    f"ASN1 Curve: {x509.get_pubkey().type()}\n"
                    f"NIST Curve: {x509.get_pubkey().bits()} bits\n"
                    f"Expires: {datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ').strftime('%d %B %Y')}\n"
                    f"Renewed: {datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ').strftime('%d %B %Y')}\n"
                    f"Serial Number: {x509.get_serial_number()}\n"
                    f"Fingerprint: {':'.join(x509.digest('sha256').decode('utf-8')[i:i+2] for i in range(0, len(x509.digest('sha256').decode('utf-8')), 2))}\n"
                )
        return result
                
    except Exception as e:
        return f"An error occurred: {e}"

async def main(url):
    
    result = get_ssl_certificate_info(url)
    return result
   
