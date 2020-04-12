import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import html.parser
import csv
from googletrans import Translator
#from translate import Translator

class StockTrack(object):
    """Provided a stock symbol find its current price."""
    def __init__(self, symbol, preferred_language, preferred_currency):
        super(StockTrack, self).__init__()
        self.symbol = symbol
        self.preferred_language = preferred_language
        self.preferred_currency = preferred_currency
        self.stockprice = {}
        self.currencylayer_accesskey = "189de90f4e628614d07092e5467483a2"
        self.fixeraccesskey = "d3024595d962553e437d1c9a6948dc55"

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
            self.stockprice['current_price'] = price
            return self.stockprice
        else:
            error = "Invalid stock symbol: {}".format(self.symbol)
            return error

    def getConversationRateLayer(self):
        url = "http://apilayer.net/api/live?access_key={}&currencies={}&source=USD&format=1".format(self.currencylayer_accesskey, self.preferred_currency)
        req = requests.get(url)
        rate_data = req.json()
        if rate_data['success'] == False:
            error = 'Query failed'
            return error
        else:
            rate = rate_data['quotes']['USD{}'.format(self.preferred_currency)]
            return rate

    def getConversationRateFixer(self):
        #FOR THE FREE PLAN, BASE "USD" IS NOT SUPPORTED THUS FOR OUR APP ITS NOT HELPFUL
        url = "http://data.fixer.io/api/latest?access_key={}&base=USD&symbols={}".format(self.fixeraccesskey, self.preferred_currency)
        req = requests.get(url)
        rate_data = req.json()
        if rate_data['success'] == False:
            error = 'Query failed'
            return error
        else:
            rate = rate_data['quotes']['USD{}'.format(self.preferred_currency)]
            return rate

    def convertToPreferredCurrency(self):
        self.processGoogleQuery()
        price = self.stockprice['current_price']
        conversion_rate = self.getConversationRateLayer()
        result = float(price) * conversion_rate
        self.stockprice['current_price'] = '{} {}'.format(result, self.preferred_currency)
        return result


    def convertLanguageToPreferred(self):
        preferred_price = self.convertToPreferredCurrency()
        response = "The current price for {} is {} {}".format(self.symbol, preferred_price, self.preferred_currency)
        translator = Translator()
        result = translator.translate(response, dest=self.preferred_language)
        return result.text




#DISPLAY SUPPORTED CURRENCIES.
def readAvailableCurrencies():
    supportedCurrency = {}
    with open('Cheap.Stocks.Internationalization.Currencies.csv', newline='') as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
           country = row["Country"]
           currency = row["Currency"]
           code = row["ISO 4217 Code"]
           complete = currency + ", symbol = " + code
           supportedCurrency[country] = complete
    return supportedCurrency

supportedCurrency = readAvailableCurrencies()
print("Supported Currencies are: {}".format(supportedCurrency))
print('\n')

#DISPLAY SUPPORTED LANGUAGES
def readAvailableLanguages():
    supportedLanguage = {}
    with open('Cheap.Stocks.Internationalization.Languages.csv', newline='') as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
           language = row["Language"]
           iso_code = row["ISO 639-1 code"]
           supportedLanguage[iso_code] = language
    return supportedLanguage
supportedLanguage = readAvailableLanguages()
print("Available Languages are: {}".format(supportedLanguage))


#REQUEST FOR USER INPUTS FOR PROCESSING
stock_symbol = input ("Enter stock symbol (kindly note only USA Stocks eg aapl) :")
preferred_language = input ("What is your preferred language:")
preferred_currency = input ("What is your preferred currency:")
stockprice = StockTrack(stock_symbol, preferred_language, preferred_currency)
results = stockprice.convertLanguageToPreferred()
print (results)



#TEST API FUNCTIONS AND TRANSLATOR

# def getConversationRateLayer():
#     url = "http://apilayer.net/api/live?access_key=189de90f4e628614d07092e5467483a2&currencies=DZD&source=USD&format=1"
#     req = requests.get(url)
#     rate_data = req.json()
#     if rate_data['success'] == False:
#         error = 'Query failed'
#         return error
#     else:
#         rate = rate_data['quotes']['USDDZD']
#         return rate
#
#
# def getConversationRateFixer():
#     #FOR THE FREE PLAN, BASE USD IS NOT SUPPORTED THUS FOR OUR APP ITS NOT HELPFUL
#     url = "http://data.fixer.io/api/latest?access_key=bf1169a26f96a42fa5ac213e45b19196&base=USD&symbols=DZD"
#     req = requests.get(url)
#     rate_data = req.json()
#     if rate_data['success'] == False:
#         error = 'Query failed'
#         return error
#     else:
#         rate = rate_data['quotes']['USDDZD']
#         return rate
#
# def convertLanguageToPreferred():
#     response = "The current price for AAPL is"
#     translator = Translator()
#     result = translator.translate(response, dest='fr')
#     return result.text
#
#
# result = convertLanguageToPreferred()
# print(result)
