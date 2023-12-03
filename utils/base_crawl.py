import os
from bs4 import BeautifulSoup
import requests
import base64
import time

from unidecode import unidecode



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
    results = soup.findAll('img', {'class': 'rg_i'}, limit=num_imgs)
    
    
    print(results)
    img_links = []
    
    for result in results:
        base64Img = result["src"]
        img_links.append(base64Img)
        
        with open('image_data.txt', 'w') as f:
            for base64Img in img_links:
                f.write(base64Img)
        
        print(f"Fount {len(img_links)} images")
        print("Start downloading...")
        
        query_folder_name = "_".join(unidecode(query).split(" "))
        SAVE_FOLDER = f"{root_folder}/{query_folder_name}_{int(time.time())}"
        
        print(SAVE_FOLDER)
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)
            
        for i, imgString in enumerate(img_links):
            img_data = getBase64(imgString)
            
            filename = f"{SAVE_FOLDER}/{query_folder_name}_{i+1}.jpg"
            
            save_image(filename, img_data)
    

class ImageCrawlBase:
    
    def __init__(self):
        pass
    
    def craw(self, queries = [], sources = [], root_folder=None):
        
        for query in queries:        
            query_str = query.get("query_str")
            limit = query.get("limit")
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