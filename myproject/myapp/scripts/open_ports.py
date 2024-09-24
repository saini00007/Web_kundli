from scapy.all import *
from urllib.parse import urlparse
import socket
import asyncio

def get_domain_from_url(url):
    parsed_uri = urlparse(url)
    domain = parsed_uri.netloc
    return domain

def get_open_ports(ip):
    open_ports = []
    ports_range = range(1, 1025)
    
    # Perform a SYN scan to discover open ports
    responses, _ = sr(IP(dst=ip)/TCP(dport=ports_range, flags="S"), timeout=1, verbose=False)
    
    # Parse the responses to find open ports
    for response in responses:
        if response[1].haslayer(TCP) and response[1][TCP].flags == 18:  # SYN-ACK
            open_ports.append(response[1][TCP].sport)
    
    return open_ports

def format_open_ports_result(open_ports):
    formatted_result = ""
   
    
   
    if open_ports:
        for port in open_ports:
            formatted_result += f"Port {port} is open  \n"
    else:
        formatted_result += "  No open ports found.\n"
    
    return formatted_result

async def main(url):
    domain = get_domain_from_url(url)
    
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror as e:
        return f"Error resolving domain: {e}"
    
    try:
        open_ports = get_open_ports(ip)
    except Exception as e:
        return f"Error during port scanning: {e}"
    
    result = format_open_ports_result(open_ports)
    return result

