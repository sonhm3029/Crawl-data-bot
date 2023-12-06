import os
from bs4 import BeautifulSoup
import requests
import base64
import time
from tqdm import tqdm 
import re

from .file import secure_filename, generateUniquePrefix



GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

def getBase64(img_data):
    head, data = img_data.split(",", 1)
    
    # Get the gile extension (gif, jpeg, png)
    file_ext = head.split(";")[0].split("/")[1]
    
    print(file_ext)
    
    # Decode the image data
    plain_data = base64.b64decode(data)
    
    return plain_data

def save_image(filename, data):
   try:
        with open(filename, 'wb') as f:
            f.write(data)
        print(f"Write {filename} successfully!")
   except Exception as e:
        print(f"Write {filename} error: {str(e) or 'Smt wrong has been occur!'}")


def bs4_request(query, num_imgs=10, root_folder="./downloads"):
    
    search_url = f"{GOOGLE_IMAGE}q={query}"
    print(f"Searching for {search_url}")
    
    
    res = requests.get(search_url, headers=usr_agent)
    html = res.content
    
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', {'class': 'isv-r PNCib ViTmJb BUooTd'})
    
    image_urls = []
    pattern_template =r'\[0,"{}",\["([^"]+)",\d+,\d+\],\["([^"]+)",\d+,\d+\]'
    for elem in tqdm(results, desc="Extract link images", unit="elem"):
        try:
            data_tbnid = elem.get("data-tbnid")
            pattern = pattern_template.format(re.escape(data_tbnid))
            matches = re.findall(pattern, str(html))
            for match in matches:
                thumbnal_img = match[0]
                full_res_img = match[1]
                image_urls.append(full_res_img)
        except Exception as e:
            print(f"ERROR extract {elem.get('data-tbnid')}: {str(e)}")
    
    print(f"Found {len(image_urls)} images")
    
    saved_folder = os.path.join(root_folder, secure_filename(query))
    if not os.path.exists(saved_folder):
        os.makedirs(saved_folder)
    
    print("Starting to download...")
    count = 0
    # Download and save images
    for i, img_url in enumerate(tqdm(image_urls, desc='Downloading images', unit='image')):
        try:
            img_data = requests.get(img_url, timeout=60).content
            with open(os.path.join(saved_folder, f"image_{i+1}_{generateUniquePrefix()}.jpg"), 'wb') as f:
                f.write(img_data)
            count +=1
            if count == num_imgs:
                break
        except Exception as e:
            print(f"Error downloading image {i + 1}: {e}")
            pass
    print(f"Download sucess {count}/{len(image_urls)}")
    

class ImageCrawlBase:
    
    def __init__(self):
        pass
    
    def craw(self, queries = [], sources = [], root_folder=None):
        
        for query in queries:        
            query_str = query.get("query_str")
            limit = query.get("limits")
            bs4_request(query_str, limit, root_folder)
            
    def craw_scheduler(self):
        pass
    
    
class TextCrawlBase:
    def __init__(self):
        pass
    
    def craw(self, queries = [], sources = [], root_folder=None):
        pass
    
    def craw_scheduler(self):
        pass