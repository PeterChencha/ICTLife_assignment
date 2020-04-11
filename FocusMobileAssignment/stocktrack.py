import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import html.parser
import csv

class StockTrack(object):
    """Provided a stock symbol find its current price."""
    def __init__(self, symbol):
        super(StockTrack, self).__init__()
        self.symbol = symbol
        self.stockprice = {}
        self.languages = {}
        self.supportedCurrency = {}

    def readAvailableLanguages(self):
        with open('Cheap.Stocks.Internationalization.Languages.csv', newline='') as csvfile:
           reader = csv.DictReader(csvfile)
           #headers = next(reader) SKIP HEADERS
           for row in reader:
               language = row["Language"]
               iso_code = row["ISO 639-1 code"]
               self.languages[iso_code] = language
        return (self.languages)

    def readAvailableCurrencies(self):
        pass

    def createGoogleQuery(self):
        #CONSTRUCT THE GOOGLE QUERY AND SUBMIT QUERY
        url = "https://www.google.com/search?tbm=fin&q={}".format(self.symbol)
        #print (url)
        try:
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0')
            resp = urlopen(req)
            html = resp.read().decode('utf-8')
            return html
        except:
            print("Error Opening the Url")

    def processGoogleQuery(self):
        #PROCESS THE RESULTS OF THE QUERY USING REGEX
        unprocessed_query = self.createGoogleQuery()
        pattern = '><span class="(.*?)" jsdata="(.*?)" jsname="(.*?)">(?:\d+(?:\.\d*)?|\.\d+)'
        list_of_items = re.search(pattern, unprocessed_query)
        if list_of_items:
            span_with_price = list_of_items.group(0)
            price = span_with_price[-6:]
            self.stockprice['name'] = self.symbol
            self.stockprice['current_price'] = '{} USD'.format(price)
            return self.stockprice
        else:
            error = "Invalid stock symbol: {}".format(self.symbol)
            return error



#GOOGLE IMPLEMENTATION
input = input ("Enter stock symbol (kindly note only USA Stocks eg aapl) :")
stockprice = StockTrack(input)
results = stockprice.readAvailableLanguages()
print (results)



# #YAHOO IMPLEMENTATION
# input = input ("Enter stock symbol :")
#stockprice = StockTrack(input)
# results = stockprice.processYahooQuery()
# print (results)
