import sys

import pymysql
from decimal import *
import logging
import time
from datetime import datetime
import os
from urllib.request import urlretrieve
import csv


from pymysql import DataError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
MYSQL = {'host': 'localhost', 'user': 'root', 'password': '123456', 'database': 'stock_db','charset':'gbk'}
# DATE_BEGIN = 'None'
DATE_BEGIN = '20100303'

# DATA_PATH = "/home/pi/"


DATA_PATH = "D:\PythonProject\StockData_System\股票数据/"


def reformat_field(record):

    stock_raw = dict()
    stock_raw['date'] = record[0]
    stock_raw['code'] = str(record[1]).lstrip("'")
    stock_raw['name'] = record[2]
    stock_raw['t_close'] = Decimal(record[3])
    stock_raw['high'] = Decimal(record[4])
    stock_raw['low'] = Decimal(record[5])
    stock_raw['t_open'] = Decimal(record[6])
    stock_raw['l_close'] = Decimal(record[7])
    stock_raw['chg'] = handle_none(record[8])
    stock_raw['p_chg'] = handle_none(record[9])
    stock_raw['turnover'] = Decimal(record[10])
    stock_raw['vo_turnover'] = Decimal(record[11])
    stock_raw['va_turnover'] = Decimal(record[12])
    stock_raw['t_cap'] = Decimal(record[13])
    stock_raw['m_cap'] = Decimal(record[14])
    return stock_raw


def handle_none(field):
    if field == 'None':
        return Decimal(0.0)
    else:
        return Decimal(field)


class DB(object):
    db = None

    def __init__(self):
        self.logger = logging.getLogger("stock_db")

        self.db = pymysql.connect(**MYSQL)
        self.start_date = self.get_start_date(DATE_BEGIN)
        today = datetime.today()
        self.end_date = today.strftime('%Y%m%d')
        self.path = DATA_PATH.__add__(self.start_date).__add__("_").__add__(self.end_date)
        if os.path.exists(self.path):
            pass
        else:
            os.mkdir(self.path)

    def save_stock_raw(self, record):
        stock_raw = reformat_field(record)
        query = """select id from stock_raw where date=%(date)s and code=%(code)s"""
        sql = """INSERT INTO stock_raw(date,
                      code, name, t_close, high,low,t_open,l_close,chg,p_chg,turnover,vo_turnover,va_turnover,t_cap,m_cap)
                      VALUES(%(date)s,%(code)s,%(name)s,%(t_close)s,%(high)s,%(low)s,%(t_open)s,%(l_close)s,%(chg)s,
                      %(p_chg)s,%(turnover)s,%(vo_turnover)s,%(va_turnover)s,%(t_cap)s,%(m_cap)s)"""
        cursor = self.db.cursor()
        cursor.execute(query, stock_raw)
        result = cursor.fetchone()
        if result:
            # print(result)
            pass
        else:
            try:
                self.logger.info(stock_raw)
                cursor.execute(sql, stock_raw)
            except DataError:
                self.logger.error(record)
        pass

    def parse_reader_and_save(self, csv_reader):
        for row in csv_reader:
            if csv_reader.line_num == 1:
                pass
            else:
                self.save_stock_raw(row)

    def close_db(self):
        self.db.close()

    def commit_db(self):
        self.db.commit()

    def last_update(self):
        sql = """SELECT date FROM stock_raw order by date desc limit 1"""
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        return result[0]

    def download_stock_csv(self, code_names):

        total = len(code_names)
        d = 0
        self.logger.info("预计下载总数cvs：{}".format(total))
        for i in range(d, len(code_names)):
            code_name = code_names[i]
            code = code_name[str.find(code_name, '(') + 1:len(code_name) - 1]
            if str.startswith(code, '6'):
                self.build_download_url(code, '0')
            if str.startswith(code, '0'):
                self.build_download_url(code, '1')
            d += 1
            self.logger.info("完成{}/{}".format(d, total))
        self.logger.info("完成所有下载")

    def build_download_url(self, code, prefix_code):
        download_url = "http://quotes.money.163.com/service/chddata.html?code="\
                       + prefix_code + code + "&start=" + \
                       self.start_date + "&end=" + self.end_date + \
                       "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;" \
                       "TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        self.write_local_csv(code, download_url)

    def write_local_csv(self, code, url):
        self.logger.info("正在下载:{}.csv".format(code))
        t0 = time.time()
        file_path = self.path.__add__('/').__add__(code).__add__(".csv")
        try:
            urlretrieve(url, file_path)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            self.write_local_csv(code, url)

        self.logger.info("下载完成:{}.csv 耗时：{}".format(code, time.time() - t0))

    def get_start_date(self, _default):
        if _default == 'None':
            result = self.last_update().strftime("%Y%m%d")
            return result

        return _default

    def read_csv_dir(self):
        self.logger.info("开始扫描入库")
        t0 = time.time()
        path = self.path
        file_names = os.listdir(path)
        for file_name in file_names:
            if file_name.endswith('.csv'):
                with open(path + "/" + file_name, newline='') as f:
                    csv_reader = csv.reader(f)
                    self.parse_reader_and_save(csv_reader)
                    self.commit_db()
                    self.logger.info("完成入库：{}".format(file_name))
        self.close_db()
        self.logger.info("入库完成总数：{} 耗时:{}s".format(len(file_names), time.time() - t0))


if __name__ == '__main__':
    db = DB()
    #db.download_stock_csv()
    db.read_csv_dir()

    pass
