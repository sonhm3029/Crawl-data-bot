import os
import urllib.request
from bs4 import BeautifulSoup
import requests
import base64
import time
from tqdm import tqdm 
import re
from pymongo import MongoClient
from dotenv import load_dotenv
<<<<<<< Updated upstream
import multiprocessing
import concurrent.futures
=======
import urllib
>>>>>>> Stashed changes

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
load_dotenv()

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
        """Crawl scheduler"""
    
    
class TextCrawlBase:
    def __init__(self, is_multi_process=False, max_workers=8):
        self.db = self.connect_db()
        self.is_multi_process = is_multi_process
        self.max_workers = max_workers
        
    def connect_db(self):
        try:
            mongoclient = MongoClient(os.environ["DB_URL"])
            db = mongoclient["crawl"]
            
            return db
        except Exception as e:
            print("ERROR connect database: ", str(e))
    
    def crawl_url(self, source, summary, title, category):
        try:
            
            exist_data = self.db["medical"].find({"url": source})
            if len(list(exist_data)):
                print(f"Exist crawl data from url {source}")
                return
            
            res = requests.get(source, headers=usr_agent)
            html = res.content
            
            soup = BeautifulSoup(html, 'html.parser')

            results = soup.find_all('div', {'class': 'streamfield'})
            collection = self.db["medical"]

            insert_data = []
            for result in results:
                insert_data.append({
                    "text": str(result),
                    "url": source,
                    "title": title,
                    "summary": summary,
                    "category": category
                })
            
            collection.insert_many(insert_data)
            
        except Exception as e:
            print(f"\nERROR crawl data url: {source} - ", str(e))
            with open("error_list.txt", "a") as f:
                f.write(f"\n{source}")
      
    def crawl_source(self, source):
        
        root_url =  "https://www.vinmec.com/vi"
        num_page = source.get("num_pages")
        url = source.get("url")
        category = source.get("category")
        print(f"Start crawling from  {url}...")
        start_page = 1
        if "https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/suc-khoe-tong-quat/" in url:
            start_page = 128 + 102
        for page in tqdm(range(start_page, num_page + 1), desc="Crawl page", unit="page"):
            try:
                url_with_page = f"{url}?page={page}"
                page_html = requests.get(url_with_page, headers=usr_agent)
                page_html = page_html.content
                
                soup = BeautifulSoup(page_html, 'html.parser')
                # Find the ul tag inside the post_list_div
                ul_tag = soup.select_one("div.post-list ul")
                li_tags = ul_tag.find_all("li")

                for li in li_tags:
                    a_tag = li.find("a")
                    post_content = li.find("div", {"class": "post-content"})
                    title = ""
                    summary = ""
                    if post_content:
                        title = post_content.find("h2").find("a")
                        if title:
                            title = title.get_text(strip=True)
                        summary = post_content.get_text(strip=True)
                        
                    if a_tag and a_tag.get("href"):
                        self.crawl_url(f"{root_url}{a_tag.get('href')}", summary, title, category)
                time.sleep(1)
            except Exception as e:
                print(f"\nError crawl source - {source}- page: {page}: {str(e)}")     
                with open("Error_page.txt", "a") as f:
                    f.write(f"\n{source.get('url')}?page={page}") 
        
            
    def crawl_one_cpu(self, sources=[]):
        try:
            for source in tqdm(sources, desc="Extracting from source"):
                self.crawl_source(source)
        except Exception as e:
            print("\nERROR crawl data - ", str(e))
        
    def crawl_mp(self, sources=[]):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                executor.map(self.crawl_source, sources)
        except Exception as e:
            print("Error crawl data - ", str(e))
        
    def crawl(self, sources=[]):
        if self.is_multi_process:
            self.crawl_mp(sources)
        else:
            self.crawl_one_cpu(sources)
            
    
    def craw_scheduler(self):
        """Crawl scheduler"""