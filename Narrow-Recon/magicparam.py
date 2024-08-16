import re
import json
import requests
import random
from urllib.parse import urlparse, parse_qsl
from bs4 import BeautifulSoup

# List of common User-Agent strings for different browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36"
]

def get_random_user_agent():
    """Return a random User-Agent string from the list."""
    return random.choice(USER_AGENTS)

def extract_params_from_url(url):
    """Extract and print query parameters from a URL."""
    parsed = urlparse(url)
    params = parse_qsl(parsed.query)
    for param_name, _ in params:
        print(param_name)

def extract_js_variables(page_html):
    """Extract and print JavaScript variable names and JSON keys from inline scripts."""
    all_script_tags = page_html.find_all("script")
    internal_js = [script for script in all_script_tags if not script.has_attr("src")]
    pattern_js = r"(?:var|let|const)\s+(\w+)\s*=\s*(.*?);"
    
    for script in internal_js:
        matches_js = re.findall(pattern_js, str(script), re.DOTALL)
        for var_name, var_value in matches_js:
            print(var_name)
            if var_value.startswith("{"):
                try:
                    parsed_data = json.loads(var_value)
                    extract_json_keys(parsed_data)
                except json.JSONDecodeError:
                    pass

def extract_form_inputs(soup):
    """Extract and print input names and IDs from forms."""
    inputs = soup.find_all('input')
    for input_tag in inputs:
        input_name = input_tag.get('name')
        input_id = input_tag.get('id')
        print(input_name)
        print(input_id)

def extract_json_keys(data):
    """Recursively extract and print subkeys from JSON data without parent keys."""
    if isinstance(data, dict):
        for key, value in data.items():
            print(key)
            if isinstance(value, dict):
                extract_json_keys(value)
            elif isinstance(value, list):
                for item in value:
                    extract_json_keys(item)
    elif isinstance(data, list):
        for item in data:
            extract_json_keys(item)

def extract_json_keys_from_response(response):
    """Extract and print JSON keys if the response content is JSON."""
    try:
        json_data = response.json()
        extract_json_keys(json_data)
    except json.JSONDecodeError:
        pass

def process_links(file_path):
    """Process each link in the file to extract and print href params, JS vars, form inputs, and JSON keys."""
    
    # Initialize a session to handle cookies and persistent settings
    session = requests.Session()
    session.headers.update({
        "User-Agent": get_random_user_agent()
    })

    with open(file_path, "r") as f:
        links = f.readlines()

    for link in links:
        url = link.strip()
        response = session.get(url)
        
        # Extract JSON keys if response is JSON
        extract_json_keys_from_response(response)
        
        page_html = BeautifulSoup(response.text, 'html.parser')
        
        # Extract href parameters
        pattern_href = r'href="([^"]+)"'
        matches_href = re.findall(pattern_href, response.text)
        for href in matches_href:
            extract_params_from_url(href)
        
        # Extract JavaScript variables
        extract_js_variables(page_html)
        
        # Extract form input names and IDs
        extract_form_inputs(page_html)

# Run the process
process_links("links.narrow")














