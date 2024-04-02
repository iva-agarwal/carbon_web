import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
import re
import base64

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

from webdriver_manager.chrome import ChromeDriverManager



# Constants
nonrenw_energytocarbon = 441 #g/kWh
renw_energytocarbon = 50 #g/kWh
datatoenergy = 0.81 #kWh/GB





def fetch_resource_size(resource_url):
    response = requests.get(resource_url)
    if response.status_code == 200:
        content_length = response.headers.get('Content-Length')
        if content_length:
          return int(content_length)
        else:
          return len(response.content)
    else:
        return 0






def getsource(tag):
    src = None
    if not src: src = tag.get('src')
    if not src: src = tag.get('data-src')
    if not src: src = tag.get('data-gt-lazy-src')
    if not src: src = tag.get('href')
    if not src: src = tag.get('xlink:href')
    if not src: src = tag.get('poster')
    if not src: src = tag.get('srcset')
    if not src: src = tag.get('data-url')
    if not src: src = tag.get('data-example')
    if not src: src = tag.get('action')
    if src:
        if src.startswith("data:image/"): return None
    return src





def calculate_data_transfer(url):
    css_size_bytes = 0
    font_size_bytes = 0
    js_size_bytes = 0
    media_size_bytes = 0
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')
    if True:
        html_size_bytes = len(html_content)
        # Fetch CSS files and estimate data transfer
        for link_tag in soup.find_all('link', rel='stylesheet'):
            src = getsource(link_tag)
            if src:
                css_url = urljoin(url, src)
                css_content = requests.get(css_url).content
                css_size_bytes += len(css_content)
                # Parse CSS content to find resource URLs and font file URLs
                resource_and_font_urls = re.findall(r'url\((.*?)\)', css_content.decode('utf-8'))
                for res_or_font_url in resource_and_font_urls:
                    abs_url = urljoin(css_url, res_or_font_url.strip('\'"'))
                    if abs_url.startswith('data:'):
                        continue
                    resource_or_font_size = fetch_resource_size(abs_url)
                    font_size_bytes += resource_or_font_size
                    
        # Fetch JS files and estimate data transfer
        for script_tag in soup.find_all('script'):
            src = getsource(script_tag)
            if src:
                js_url = urljoin(url, src)
                js_content = requests.get(js_url).content
                js_size_bytes += len(js_content)
                
                # Parse JS content to find video and audio URLs
                resource_urls = re.findall(r'src="(.*?)"', js_content.decode('utf-8'))
                for res_url in resource_urls:
                    if res_url.startswith(('data:', 'about:')):
                        continue  # Skip data URI schemes
                    abs_url = urljoin(js_url, res_url)
                    res_size = fetch_resource_size(abs_url)
                    js_size_bytes += res_size
                    
        # Fetch video and audio elements
        for video_tag in soup.find_all('video'):
            src = getsource(video_tag)
            if src:
                video_url = urljoin(url, src)
                video_size = fetch_resource_size(video_url)
                media_size_bytes += video_size

        
        for audio_tag in soup.find_all('audio'):
            src = getsource(audio_tag)
            if src:
                audio_url = urljoin(url, src)
                audio_size = fetch_resource_size(audio_url)
                media_size_bytes += audio_size

        for img_tag in soup.find_all('img'):
            src = getsource(img_tag)
            if src:
                image_url = urljoin(url, src)
                image_size = fetch_resource_size(image_url)
                media_size_bytes += image_size
        
        css_transfer_gb = css_size_bytes / (1024 ** 3)
        font_transfer_gb = font_size_bytes / (1024 ** 3)
        js_transfer_gb = js_size_bytes / (1024 ** 3)
        media_transfer_gb = media_size_bytes / (1024 ** 3)
        html_transfer_gb = html_size_bytes / (1024 ** 3)
        return css_transfer_gb, font_transfer_gb, js_transfer_gb, media_transfer_gb, html_transfer_gb
    else:
        raise Exception(f"Failed to fetch website content. Status code: {response.status_code}")






def check_green_website(url):
    parsed_url = urlparse(url).netloc
    url = f"https://api.thegreenwebfoundation.org/api/v3/greencheck/"+parsed_url
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["green"]
    else:
        return False






def calculate_carbon(data,green):
    if green is True:
        return renw_energytocarbon*datatoenergy*data
    else:
        return nonrenw_energytocarbon*datatoenergy*data






def calculate_footprint(web_url):
    try:
        data_gb = calculate_data_transfer(web_url)
        totat_data = sum(data_gb)
        green = check_green_website(web_url)
        carbon = calculate_carbon(totat_data, green)
    except Exception as e:
        print(e)
    result = {
        'css_data_gb': data_gb[0],
        'font_data_gb': data_gb[1],
        'js_data_gb': data_gb[2],
        'media_data_gb': data_gb[3],
        'html_data_gb': data_gb[4],
        'total_data_gb': totat_data,
        'Carbon_footprint':carbon,
        'Green_hosting': green,
    }
    return result
