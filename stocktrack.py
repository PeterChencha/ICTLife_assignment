import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

class StockTrack(object):
    """Provided a stock symbol find its current price."""
    def __init__(self, symbol):
        super(StockTrack, self).__init__()
        self.symbol = symbol
        self.stockprice = {}

    def createYahooQuery(self):
        url = "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch".format(self.symbol, self.symbol)
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
            self.stockprice['name'] = self.symbol
            self.stockprice['current_price'] = '{}USD'.format(price)
            return self.stockprice
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
        sections = unprocessed_info.find_all('g')
        #print (sections)
        return sections
        #price = unprocessed_info.find('div',{'id': 'center_col'}).find('span').text
        #print (unprocessed_info)

        # try:
        #     self.price['name'] = sections[0].div.text
        #     spans = sections[1].find_all('div', recursive=False)[1].find_all('span', recursive=False)
        #     self.price['current_price'] = spans[0].text
        #     self.price['current_change'] = spans[1].text
        #     return self.price
        # except:
        #     error = "Not the div we want"
        #     return error




#GOOGLE IMPLEMENTATION
# input = input ("Enter stock symbol :")
# stockprice = StockTrack(input)
# results = stockprice.processGoogleQuery()
# print (results)



#YAHOO IMPLEMENTATION
input = input ("Enter stock symbol :")
stockprice = StockTrack(input)
results = stockprice.processYahooQuery()
print (results)
