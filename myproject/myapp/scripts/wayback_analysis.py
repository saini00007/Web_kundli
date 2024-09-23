import aiohttp
import asyncio
from datetime import datetime
from statistics import mean

# Functions to process the wayback data

def convert_timestamp_to_date(timestamp):
    year = int(timestamp[0:4])
    month = int(timestamp[4:6])
    day = int(timestamp[6:8])
    hour = int(timestamp[8:10])
    minute = int(timestamp[10:12])
    second = int(timestamp[12:14])
    return datetime(year, month, day, hour, minute, second)

def count_page_changes(results):
    prev_digest = None
    change_count = 0
    for result in results:
        if result[2] != prev_digest:
            change_count += 1
            prev_digest = result[2]
    return change_count

def get_average_page_size(scans):
    sizes = [int(scan[3]) for scan in scans]
    return round(mean(sizes))

def get_scan_frequency(first_scan, last_scan, total_scans, change_count):
    days_between_scans = (last_scan - first_scan).days / total_scans
    days_between_changes = (last_scan - first_scan).days / change_count
    scans_per_day = (total_scans - 1) / (last_scan - first_scan).days
    changes_per_day = change_count / (last_scan - first_scan).days
    return {
        'Days Between Scans': round(days_between_scans, 2),
        'Days Between Changes': round(days_between_changes, 2),
        'Scans Per Day': round(scans_per_day, 2),
        'Changes Per Day': round(changes_per_day, 2)
    }

async def fetch_wayback_data(session, url):
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp,statuscode,digest,length,offset"

    try:
        async with session.get(cdx_url) as response:
            data = await response.json()
            if not data or not isinstance(data, list) or len(data) <= 1:
                return {'skipped': 'Site has never been archived via the Wayback Machine'}

            data.pop(0)

            first_scan = convert_timestamp_to_date(data[0][0])
            last_scan = convert_timestamp_to_date(data[-1][0])
            total_scans = len(data)
            change_count = count_page_changes(data)
            average_page_size = get_average_page_size(data)
            scan_frequency = get_scan_frequency(first_scan, last_scan, total_scans, change_count)

            return {
                'First Scan': first_scan.strftime("%Y-%m-%d %H:%M:%S"),
                'Last Scan': last_scan.strftime("%Y-%m-%d %H:%M:%S"),
                'Total Scans': total_scans,
                'Change Count': change_count,
                'Avg Size': average_page_size,
                'Avg Scans per Day': scan_frequency['Scans Per Day']
            }
    except Exception as e:
        return {'error': f'Error fetching Wayback data: {str(e)}'}

async def run_wayback_analysis(url):
    async with aiohttp.ClientSession() as session:
        result = await fetch_wayback_data(session, url)
        return result

async def main(url):
    try:
        result = await asyncio.wait_for(run_wayback_analysis(url), timeout=20)
        return format_result(result)
    except asyncio.TimeoutError:
        return "Error:Operation timed out ."

def format_result(result):
    # Create output suitable for HTML display
    output = ""
    if 'error' in result:
        output += f"Error: {result['error']}"
        return output

    if 'skipped' in result:
        output += f"Skipped: {result['skipped']}"
        return output

    
    for key, value in result.items():
        output += f"{key}: {value}"
    

    return output