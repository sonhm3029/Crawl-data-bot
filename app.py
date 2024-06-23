from utils.base_crawl import ImageCrawlBase


crawler = ImageCrawlBase()

if __name__ == "__main__":
    crawler.craw([
        {"query_str": "gather+at+beer", "limits": 100},
        # {"query_str": "gather+at+beer+in+vietnam", "limits": 100},
        # {"query_str": "uống bia ở việt nam", "limits": "100"}
        # {"query_str": "uống bia heineken", "limits": 50},
        # {"query_str": "uống bia heineken", "limits": 50}
    
    ], root_folder=r"C:\Users\hoang\OneDrive\Desktop\nghich_prj\crawl_data_bot\downloads")