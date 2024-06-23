from icrawler.builtin import GoogleImageCrawler
from utils.file import secure_filename, generateUniquePrefix
import os

queries = [
    ("Heineken beer can", 30),
    ("Heineken beer bottle", 30),
    ("Heineken beer", 30),
    ("Tiger beer can", 30),
    ("Tiger beer bottle", 30),
    ("Tiger beer", 30),
    ("Bia Việt can", 30),
    ("Bia Việt bottle", 30),
    ("Bia Việt", 30),
    ("Larue beer can", 30),
    ("Larue beer bottle", 30),
    ("Larue beer", 30),
    ("Bivina beer can", 30),
    ("Bivina beer bottle", 30),
    ("Bivina beer", 30),
    ("Edelweiss beer can", 30),
    ("Edelweiss beer bottle", 30),
    ("Edelweiss beer", 30),
    ("Strongbow can", 30),
    ("Strongbow bottle", 30),
    ("Strongbow cider", 30),
    ("Sài Gòn beer can", 30),
    ("Sài Gòn beer bottle", 30),
    ("Sài Gòn beer", 30),
    ("333 beer can", 30),
    ("333 beer bottle", 30),
    ("333 beer", 30),
    ("Huda beer can", 30),
    ("Huda beer bottle", 30),
    ("Huda beer", 30)
]


root = "icrawler_downloads"


for query, max_num in queries:
    download_root = secure_filename(query)
    download_root = os.path.join(root, download_root)
    if not os.path.exists(download_root):
        os.makedirs(download_root)
    bing_crawler = GoogleImageCrawler(storage={'root_dir': download_root})
    bing_crawler.crawl(keyword=query, max_num=max_num)
