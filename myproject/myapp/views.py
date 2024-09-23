from django.shortcuts import render
import asyncio

# Import your async and sync scripts here
from .scripts.block_detection import handler as block
from .scripts.wayback_analysis import main as run_wayback_analysis
from .scripts.carbon import run_carbon_footprint
from .scripts.subdomain_detection import main as subdomain_handler
from .scripts.cookies import handler as cookies_detection_handler
from .scripts.robots import get_robots_txt
from .scripts.DNS_records import get_dns_records
from .scripts.DNS_server import get_dns_server
from .scripts.dnssec_handler import get_dnssec_info
from .scripts.Email_conf import fetch_email_configurations
from .scripts.site_feature import check_site_features
from .scripts.firewall import check_and_print_waf
from .scripts.http_headers import main as header
from .scripts.HSTS import get_hsts_info
from .scripts.HTTP_security import main as HTTP
from .scripts.Linked_pages import main as Linked
from .scripts.Location import main as Location 
from .scripts.open_ports import main as open_ports
from .scripts.redirect import main as redirect 
from .scripts.Security_txt import main as Security
from .scripts.site_status import main as site 
from .scripts.social_tags import main as social
from .scripts.SSL import main as SSL
from .scripts.Web_tech import main as Web 
from .scripts.VT import main as VT
from .scripts.TLS_Cipher_suites import main as TLS 
from .scripts.web_rank import main as rank
from .scripts.TXT_records import main as TXT
from .scripts.Who_is import main as who




# Import the robots.txt handler

# Async wrapper to call sync functions in an async environment
async def run_block_detection(url):
    return await block(url)
    

async def run_wayback_analysis_wrapper(url):
    return await run_wayback_analysis(url)

async def run_carbon_footprint_wrapper(url):
    return await run_carbon_footprint(url)

async def run_subdomain_detection_wrapper(url):
    return await subdomain_handler(url)

async def run_cookies_detection_wrapper(url):
    return await cookies_detection_handler(url)

async def run_robots_txt_wrapper(url):
    return await get_robots_txt(url) 

async def run_dns_records_wrapper(url):
    return await get_dns_records(url)

async def run_dns_server_wrapper(url):
    return await get_dns_server(url)

async def run_dnssec_handler_wrapper(url):
    return await get_dnssec_info(url)

async def run_fetch_email_configurations_wrapper(url):
    return await fetch_email_configurations(url)

async def run_check_site_features_wrapper(url):
    return await check_site_features(url)

async def run_check_and_print_waf_wrapper(url):
    return await check_and_print_waf(url)

async def run_fetch_and_print_headers_wrapper(url):
    return await header(url)

async def run_get_hsts_info_wrapper(url):
    return await get_hsts_info(url)

async def run_HTTP_security_wrapper(url):
    return await HTTP(url)

async def run_Linked_pages_wrapper(url):
    return await Linked(url)

async def run_Location_wrapper(url):
    return await Location(url)

async def run_open_ports_wrapper(url):
    return await open_ports(url)

async def run_redirect_wrapper(url):
    return await redirect(url)

async def run_Security_txt_wrapper(url):
    return await Security(url)

async def run_site_status_wrapper(url):
    return site(url)

async def run_social_tags_wrapper(url):
    return await social(url)

async def run_SSL_wrapper(url):
    return await SSL(url)

async def run_Web_tech_wrapper(url):
    return await Web(url)

async def run_VT_wrapper(url):
    return await VT(url)


async def run_TLS_Cipher_suites_wrapper(url):
    return await TLS(url)

async def run_web_rank_wrapper(url):
    return await rank(url)

async def run_TXT_records_wrapper(url):
    return await TXT(url)

async def run_Who_is_wrapper(url):
    return await who(url)

# Main async function to run all scripts concurrently
async def run_all_scripts(url):
    # Running all scripts concurrently using asyncio.gather
    block_detection_result = run_block_detection(url)
    wayback_analysis_result = run_wayback_analysis_wrapper(url)
    carbon_footprint_result = run_carbon_footprint_wrapper(url)
    subdomain_detection_result = run_subdomain_detection_wrapper(url)
    cookies_detection_result = run_cookies_detection_wrapper(url)
    robots_txt_result = run_robots_txt_wrapper(url)
    dns_records_result = run_dns_records_wrapper(url)
    dns_server_result = run_dns_server_wrapper(url)
    dnssec_result = run_dnssec_handler_wrapper(url)
    Email_conf_result = run_fetch_email_configurations_wrapper(url)
    features_result = run_check_site_features_wrapper(url)
    firewall_result = run_check_and_print_waf_wrapper(url)
    headers_result = run_fetch_and_print_headers_wrapper(url)
    HSTS_result = run_get_hsts_info_wrapper(url)
    HTTP_security_result  = run_HTTP_security_wrapper(url)   
    Linked_pages_result  = run_Linked_pages_wrapper(url)
    Location_result = run_Location_wrapper(url)
    open_ports_result = run_open_ports_wrapper(url)
    redirect_result = run_redirect_wrapper(url)
    Security_txt_result = run_Security_txt_wrapper(url)
    site_status_result = run_site_status_wrapper(url)
    social_tags_result = run_social_tags_wrapper(url)
    SSL_result = run_SSL_wrapper(url)
    Web_tech_result = run_Web_tech_wrapper(url)
    VT_result = run_VT_wrapper(url)
    TLS_Cipher_suites_result = run_TLS_Cipher_suites_wrapper(url)
    web_rank_result = run_web_rank_wrapper(url)
    TXT_records_result = run_TXT_records_wrapper(url)
    Who_is_result  = run_Who_is_wrapper(url)  
                                       
    results = await asyncio.gather(
        block_detection_result,
        wayback_analysis_result,
        carbon_footprint_result,
        subdomain_detection_result,
        cookies_detection_result,
        robots_txt_result,
        dns_records_result,
        dns_server_result,
        dnssec_result,
        Email_conf_result,
        features_result,
        firewall_result,
        headers_result,
        HSTS_result,
        HTTP_security_result,
        Linked_pages_result,
        Location_result,
        open_ports_result,
        redirect_result,
        Security_txt_result,
        site_status_result,
        social_tags_result,
        SSL_result,
        Web_tech_result,
        VT_result,
        TLS_Cipher_suites_result,
        web_rank_result,
        TXT_records_result,
        Who_is_result,
        
        
        
        
        
        # Gather robots.txt result
    )

    return {
        'block_detection': results[0],
        'wayback_analysis': results[1],
        'carbon_footprint': results[2],
        'subdomain_detection': results[3],
        'cookies_detection': results[4],
        'robots_txt': results[5], 
        'dns_records': results[6],
        'dns_server': results[7],
        'dnssec': results[8],
        'email_conf': results[9],
        'features': results[10],
        'firewall': results[11],
        'headers': results[12],
        'HSTS' : results[13],
        'HTTP_security' : results[14],
        'Linked_pages' : results[15],
        'Location' : results[16],
        'open_ports' : results[17],
        'redirect' : results[18],
        'Security_txt' : results[19],
        'site_status' : results[20],
        'social_tags' : results[21],
        'SSL' : results[22],
        'Web_tech' : results[23],
        'VT' : results[24],
        'TLS_Cipher_suites' : results[25],
        'web_rank' : results[26],
        'TXT_records' : results[27],
        'Who_is' : results[28]
        
        
        
    }

# Django view to handle the POST request and run all scripts
async def run_all_scripts_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        # Run all scripts concurrently
        results = await run_all_scripts(url)

        # Render the results in a template
        return render(request, 'result.html', {'results': results})

    return render(request, 'index.html')
