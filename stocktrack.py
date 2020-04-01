import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

class StockTrack(object):
    """Provided a stock symbol find its current price."""
    def __init__(self, symbol):
        super(StockTrack, self).__init__()
        self.symbol = symbol

    def createYahooQuery(self):
        url = "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
        try:
            page = urlopen(url)
            soup = bs4.BeautifulSoup(page,'html.parser')
            price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
            return price
        except:
            print("Error Opening the Url")

    def createQuery(self):
        url = "https://google.com/search?q={self.symbol}"
        try:
            page = urlopen(url)
            soup = bs4.BeautifulSoup(page,'html.parser')
            return soup
        except:
            print("Error Opening the Url")

    def processQuery(self):
        unprocessed_info = createQuery()
        price = unprocessed_info.find('div',{'id': 'center_col'}).find('span').text



    def getPrice(self):
        try:
            if self.symbol == "aapl":
                return 254.29
            else:
                error = "Symbol not found"
                return error
        except Exception as e:
            raise e


# input = raw_input ("Enter stock symbol :")
# stockprice = StockTrack(input)
# results = stockprice.getPrice()
# print (results)

input = "aapl"
stockprice = StockTrack(input)
results = stockprice.createYahooQuery()
print (results)
