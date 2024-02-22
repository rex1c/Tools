import re , json , requests
from urllib.parse import urlparse, parse_qsl 
import urllib
from bs4 import BeautifulSoup

# href extractor
f = open("links.narrow", "r")
links = f.readlines()
for link in links:
    url = links[:-1]
    response = requests.get(url)
    pattern_href = r'href="([^"]+)"'
    matches_href = re.findall(pattern_href, response.text)

    for link in matches_href:
        parsed = urlparse(link)
        params = parse_qsl(parsed.query)
        for param_name, _ in params:
            print(param_name)

    # javascript extractor
    def page_javaScript(page_html):
        all_script_tags = page_html.find_all("script")
        internal_js = list(filter(lambda script: not script.has_attr("src"), all_script_tags))
        pattern_js = r"(?:var|let|const)\s+(\w+)\s*=\s*(.*?);"
        
        for script in internal_js:
            matches_js = re.findall(pattern_js, str(script), re.DOTALL)
            for var_name, var_value in matches_js:
                if var_value[0] == "{":
                    parsed_data = json.loads(var_value)
                    keys = parsed_data.keys()
                    for key in keys:
                        print(key)
                else:
                    pass
                print(var_name)

        

    page_html = BeautifulSoup(response.text, 'html.parser')
    page_javaScript(page_html)


    # form extractor 

    soup = BeautifulSoup(response.text, 'html.parser')
    inputs = soup.find_all('input')

    for input_tag in inputs:
        input_name = input_tag.get('name')
        input_id = input_tag.get('id')
        print(input_name)
        print(input_id)













