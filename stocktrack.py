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
        url = "https://finance.yahoo.com/quote/{}?p=AAPL&.tsrc=fin-srch".format(self.symbol)
        #print (url)
        try:
            page = urlopen(url)
            soup = bs4.BeautifulSoup(page,'html.parser')
            return soup
        except:
            print("Error Opening the Url")

    def processYahooQuery(self):
        unprocessed_info = self.createYahooQuery()
        try:
            price = unprocessed_info.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
            return price
        except:
            error = "Not the div we want"
            return error



    def createGoogleQuery(self):
        url = "https://google.com/search?q={}".format(self.symbol)
        print (url)
        try:
            resp = requests.get(url)
            soup = bs4.BeautifulSoup(resp.content,'html.parser')
            return soup
        except:
            print("Error Opening the Url")

    def processGoogleQuery(self):
        unprocessed_info = self.createGoogleQuery()
        #price = unprocessed_info.find('div',{'id': 'center_col'}).find('span').text
        #print (unprocessed_info)
        try:
            price = unprocessed_info.find('div',{'class': 'OiIFo'}).find('span').text
            return price
        except:
            error = "Not the div we want"
            return error




#GOOGLE IMPLEMENTATION
input = input ("Enter stock symbol :")
stockprice = StockTrack(input)
results = stockprice.processGoogleQuery()
print (results)



#YAHOO IMPLEMENTATION
# input = input ("Enter stock symbol :")
# stockprice = StockTrack(input)
# results = stockprice.processYahooQuery()
# print (results)
