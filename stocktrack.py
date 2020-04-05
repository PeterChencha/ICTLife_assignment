import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import html.parser
import json

class StockTrack(object):
    """Provided a stock symbol find its current price."""
    def __init__(self, symbol):
        super(StockTrack, self).__init__()
        self.symbol = symbol
        self.stockprice = {}

    def verifySymbol(self):
        if type(self.symbol) == 'str':
            return True
        else:
            return False

    def createYahooQuery(self):
        url = "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch".format(self.symbol, self.symbol)
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
            self.stockprice['name'] = self.symbol
            self.stockprice['current_price'] = '{}USD'.format(price)
            return self.stockprice
        except:
            error = "Not the div we want"
            return error



    def createGoogleQuery(self):
        url = "https://www.google.com/search?tbm=fin&q={}".format(self.symbol)
        print (url)
        try:
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0')
            resp = urlopen(req)
            html = resp.readlines()
            return html
        except:
            print("Error Opening the Url")

    def processGoogleQuery(self):
        unprocessed_query = self.createGoogleQuery()
        return unprocessed_query


#GOOGLE IMPLEMENTATION
input = input ("Enter stock symbol :")
stockprice = StockTrack(input)
results = stockprice.processGoogleQuery()
print (results)



# #YAHOO IMPLEMENTATION
# input = input ("Enter stock symbol :")
# stockprice = StockTrack(input)
# results = stockprice.processYahooQuery()
# print (results)
