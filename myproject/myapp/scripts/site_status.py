import requests

def check_server_status(url):
    try:
        response = requests.head(url)
        status = "Online" if response.status_code == 200 else "Not Known"
        status_code = response.status_code
        response_time = response.headers.get('Server-Timing', 'N/A')
        
        return {
            'status': status,
            'status_code': status_code,
            'response_time': response_time
        }
    except requests.RequestException as e:
        raise Exception("Error connecting to the server")

def format_result(result):
    output = []
    
    if 'status' in result:
        output.append(f"Server Status: {'✅' if result['status'] == 'Online' else '❌'} {result['status']}")
        output.append(f"Status Code: {result['status_code']}")
    else:
        output.append("Error: Unable to determine server status")

    return "\n".join(output)

def main(url):
    result = check_server_status(url)
    formatted_output = format_result(result)
    return formatted_output
