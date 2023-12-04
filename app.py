from utils.base_crawl import ImageCrawlBase


crawler = ImageCrawlBase()

if __name__ == "__main__":
    crawler.craw([
        {"query_str": "mèo", "limits": 10}
    ], root_folder=r"C:\Users\hoang\OneDrive\Desktop\nghich_prj\crawl_data_bot\downloads")