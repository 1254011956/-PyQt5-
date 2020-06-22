import logging

import scrapy


from  StockData_System.stockCodeSpider.stock.spiders.stock_db import DB


class MySpider(scrapy.Spider):
    name = "stock"
    Q = None

    def __init__(self):
        self.db = DB()

    def start_requests(self):
        # urls = ["https://hq.gucheng.com/gpdmylb.html"]
        #
        # for url in urls:
        #     yield scrapy.Request(url, self.parse)
        return [scrapy.Request("https://hq.gucheng.com/gpdmylb.html", self.parse)]

    def parse(self, response):
        code_names = response.xpath('//*[@id="stock_index_right"]/div[3]/section/a/text()').getall()
        '''codes = []
               d = 0
               for i in range(d, len(code_names)):
                   code_name = code_names[i]
                   code = code_name[str.find(code_name, '(') + 1:len(code_name) - 1]
                   codes.append(code)
                   with open('codes.txt', 'w') as f:
                       f.write(str(codes))
               print(codes)'''
        logging.info("stock_code 更新完成")
        self.db.download_stock_csv(code_names)
        self.db.read_csv_dir()
if __name__ == '__main__':
    db = DB()
    #db.download_stock_csv()
    db.read_csv_dir()
