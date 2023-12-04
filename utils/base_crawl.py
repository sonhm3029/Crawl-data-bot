import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import base64
import time
from tqdm import tqdm 

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

# Use ChromeDriver with Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run headless (without GUI)
driver = webdriver.Chrome(options=chrome_options)

def getBase64(img_data):
    head, data = img_data.split(",", 1)
    
    # Get the gile extension (gif, jpeg, png)
    file_ext = head.split(";")[0].split("/")[1]
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
    
    # Use Selenium to get the dynamic content
    driver.get(search_url)
    dynamic_content = driver.page_source

    # Close the Selenium-controlled browser
    driver.quit()
    soup = BeautifulSoup(dynamic_content, 'html.parser')

    results = soup.find_all('img', {'class': 'rg_i'}, limit=num_imgs)

    image_urls = [img.get('src') or img.get('data-src') for img in results]
    
    saved_folder = os.path.join(root_folder, secure_filename(query))
    print(results)
    # if not os.path.exists(saved_folder):
    #     os.makedirs(saved_folder)
    # else:
    #     with open(os.path.join("saved_folder", "list_link.txt")) as f:
            

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