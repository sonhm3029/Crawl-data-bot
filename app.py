from utils.base_crawl import ImageCrawlBase


crawler = ImageCrawlBase()

if __name__ == "__main__":
    crawler.craw([
        {"query_str": "mèo", "limits": 10}
    ], root_folder="./downloads")