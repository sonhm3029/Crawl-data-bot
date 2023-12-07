from utils.base_crawl import TextCrawlBase


if __name__ == "__main__":
    crawler = TextCrawlBase()
    crawler.crawl([
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/thong-tin-duoc/",
            "num_pages": 5,
            "category": "Thông tin dược"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/san-phu-khoa-va-ho-tro-sinh-san/",
            "num_pages": 337,
            "category": "Sản phụ khoa và hỗ trợ sinh sản"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/nhi/",
            "num_pages": 410,
            "category": "Nhi"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/suc-khoe-tong-quat/",
            "num_pages": 934,
            "category": "Sức khỏe tổng quát"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/thong-tin-suc-khoe/te-bao-goc-cong-nghe-gen/",
            "num_pages": 12,
            "category": "Công nghệ gen"
        },
        {
            "url": "https://www.vinmec.com/tin-tuc/thong-tin-suc-khoe/dinh-duong/",
            "num_pages": 249,
            "category": "Dinh dưỡng"
        },
        {
            "url": "https://www.vinmec.com/tin-tuc/thong-tin-suc-khoe/song-khoe/",
            "num_pages": 169,
            "category": "Sống khỏe"
        },
        {
            "url": "https://www.vinmec.com/tin-tuc/thong-tin-suc-khoe/lam-dep/",
            "num_pages": 95,
            "category": "Làm đẹp"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/hoat-dong-dao-tao/tieu-hoa-gan-mat/",
            "num_pages": 1,
            "category": "Tiêu hóa gan mật"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/hoat-dong-dao-tao/san-phu-khoa-va-ho-tro-sinh-san/",
            "num_pages": 1,
            "category": "Sản phụ khoa và hỗ trợ sinh sản"
        },
        {
            "url": "https://www.vinmec.com/vi/tin-tuc/hoi-dap-bac-si/",
            "num_pages": 563,
            "category": "Hỏi đáp bác sĩ"
        }
    ])         