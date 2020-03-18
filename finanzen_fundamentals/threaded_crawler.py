import threading

import requests
from lxml import html

StockMarkets = {
    "BER": {"url_postfix": "@stBoerse_BER", "real_name": "Berlin"},
    "DUS": {"url_postfix": "@stBoerse_DUS", "real_name": "Düsseldorf"},
    "FSE": {"url_postfix": "@stBoerse_FSE", "real_name": "Frankfurt Stock Exchange"},
    "HAM": {"url_postfix": "stBoerse_HAM", "real_name": "Hamburg"},
    "HAN": {"url_postfix": "@stBoerse_HAN", "real_name": "Hannover"},
    "MUN": {"url_postfix": "@stBoerse_MUN", "real_name": "München"},
    "XETRA": {"url_postfix": "@stBoerse_XETRA", "real_name": "XETRA"},
    "STU": {"url_postfix": "@stBoerse_STU", "real_name": "Stuttgard"},
    "TGT": {"url_postfix": "@stBoerse_TGT", "real_name": "Tradegate"},
    "BAE": {"url_postfix": "@stBoerse_BAE", "real_name": ""},
    "BRX": {"url_postfix": "@stBoerse_BRX", "real_name": ""},
    "BTT": {"url_postfix": "@stBoerse_BTT", "real_name": ""},
    "CLB": {"url_postfix": "@stBoerse_CLB", "real_name": ""},
    "GVIE": {"url_postfix": "@stBoerse_GVIE", "real_name": ""},
    "NAS": {"url_postfix": "@stBoerse_NAS", "real_name": ""},
    "MXK": {"url_postfix": "@stBoerse_MXK", "real_name": ""},
    "SIX": {"url_postfix": "@stBoerse_SWX", "real_name": ""},
    "XQTX": {"url_postfix": "@stBoerse_XQTX", "real_name": ""},
    "AMEX": {"url_postfix": "@stBoerse_AMEX", "real_name": ""},
    "NYSE": {"url_postfix": "@stBoerse_NYSE", "real_name": "New York Stock Exchange"},
}


class CrawlerMain:
    def __init__(self, ticker: [{}]):
        self.ticker_list = ticker
        self.results = []
        self.crawler_threads = []

        for e in self.ticker_list:
            if 'stockmarket' not in e.keys():
                e['stockmarket'] = "TGT"

            self.crawler_threads.append(CrawlerThread(ticker=str(e['ticker']), exchange=str(e['stockmarket'])))

    def run(self):
        check_results = []

        for e in self.ticker_list:
            current = CrawlerThread(ticker=str(e['ticker']), exchange=str(e['stockmarket']))
            check_results.append(current)
            current.start()

        for x in check_results:
            x.join()

            for element in x.summary_data:
                print(x.summary_data[element])


class CrawlerThread(threading.Thread):
    def __init__(self, ticker: str, exchange):
        threading.Thread.__init__(self)
        self.ticker_name = ticker
        self.exchange = exchange
        self.summary_data = {}

    def run(self):
        url = "https://www.finanzen.net/aktien/" + self.ticker_name + "-aktie" + StockMarkets[self.exchange][
            'url_postfix']
        response = requests.get(url, verify=True)

        # sleep()
        parser = html.fromstring(response.text)
        summary_table = parser.xpath('//div[contains(@class,"row quotebox")][1]')

        i = 0

        for table_data in summary_table:
            raw_price = table_data.xpath(
                '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-5")]/text()')
            raw_currency = table_data.xpath(
                '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-5")]/span//text()')
            raw_change = table_data.xpath(
                '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-4")]/text()')
            raw_percentage = table_data.xpath(
                '//div[contains(@class,"row quotebox")][1]/div[contains(@class, "col-xs-3")]/text()')
            raw_name = table_data.xpath('//div[contains(@class, "col-sm-5")]//h1/text()')
            raw_instrument_id = table_data.xpath('//span[contains(@class, "instrument-id")]/text()')
            raw_time = table_data.xpath('//div[contains(@class,"row quotebox")]/div[4]/div[1]/text()')
            raw_exchange = table_data.xpath('//div[contains(@class,"row quotebox")]/div[4]/div[2]/text()')

            name = ''.join(raw_name).strip()
            time = ''.join(raw_time).strip()
            exchange = ''.join(raw_exchange).strip()

            instrument_id = ''.join(raw_instrument_id).strip()
            (wkn, isin) = instrument_id.split(sep='/')
            if 'Symbol' in isin:
                (isin, sym) = isin.split(sep='Symbol')
            else:
                sym = ""

            currency = ''.join(raw_currency).strip()

            self.summary_data[i] = {
                "name": name.replace('&nbsp', ''),
                "wkn": wkn.replace(' ', '').replace("WKN:", ""),
                "isin": isin.replace(' ', '').replace("ISIN:", ""),
                "symbol": sym.replace(' ', '').replace(":", ""),
                "price": float(raw_price[0].replace(',', '.')),
                "currency": currency,
                "change_to_opening": float(raw_change[0].replace(',', '.')),
                "change_percentage": float(raw_percentage[0].replace(',', '.')),
                "time": time,
                "exchange": StockMarkets[exchange]['real_name']
            }

            i += 1

        return self.summary_data
