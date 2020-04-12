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
        self.errors = []

    #FOR ERROR HANDLING I'LL BE RETURNING ZERO SO THAT THE NEXT CALLED FUNCTION KNOWS THERE WAS AN ERROR IN THE FLOW
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
            error = "Error Opening the Url."
            self.errors.append(error)
            return 0

    def processGoogleQuery(self):
        #PROCESS THE RESULTS OF THE QUERY USING REGEX
        unprocessed_query = self.createGoogleQuery()
        if unprocessed_query == 0:
            return 0
        else:
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
                self.errors.append(error)
                return 0

    def getConversionRateLayer(self):
        #GET CONVERSION RATE FROM LAYER API
        url = "http://apilayer.net/api/live?access_key={}&currencies={}&source=USD&format=1".format(self.currencylayer_accesskey, self.preferred_currency)
        req = requests.get(url)
        rate_data = req.json()
        if rate_data['success'] == False:
            error = 'Conversion Query failed'
            self.errors.append(error)
            return 0
        else:
            rate = rate_data['quotes']['USD{}'.format(self.preferred_currency)]
            return rate

    def getConversionRateFixer(self):
        #FOR THE FREE PLAN, BASE "USD" IS NOT SUPPORTED THUS FOR OUR APP ITS NOT HELPFUL SINCE OUR SCRAPPED STOCKS ARE IN USD
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
        processedquery = self.processGoogleQuery()
        conversion_rate = self.getConversionRateLayer()
        if processedquery == 0 or conversion_rate == 0:
            return 0
        else:
            price = self.stockprice['current_price']
            result = float(price) * conversion_rate
            self.stockprice['current_price'] = '{} {}'.format(result, self.preferred_currency)
            return result


    def convertLanguageToPreferred(self):
        preferred_price = self.convertToPreferredCurrency()
        if preferred_price == 0:
            return self.errors
        else:
            response = "The current price for {} is".format(self.symbol)
            translator = Translator()
            result = translator.translate(response, dest=self.preferred_language)
            return result.text +" {}{}".format(preferred_price, self.preferred_currency)




#DISPLAY SUPPORTED CURRENCIES.
print('\n')
def readAvailableCurrencies():
    supportedCurrency = {}
    with open('Cheap.Stocks.Internationalization.Currencies.csv', newline='') as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
           country = row["Country"]
           currency = row["Currency"]
           code = row["ISO 4217 Code"]
           complete = currency + ", symbol = " + code
           supportedCurrency[country] = code
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
print('\n')

#REQUEST FOR USER INPUTS FOR PROCESSING. STRIP TO REMOVE WHITESPACE.
stock_symbol = input ("Enter stock symbol (kindly note only USA Stocks eg aapl or msft) :").strip()
preferred_language = input ("What is your preferred language(leave blank for english-en):").strip()
if len(preferred_language) == 0:
    preferred_language = "en"
preferred_currency = input ("What is your preferred currency(leave blank for USD):").strip()
if len(preferred_currency) == 0:
    preferred_currency = "USD"
print('\n')

#CHECK IF LANGUAGE AND CURRENCY IS SUPPORTED
if preferred_language not in supportedLanguage.keys():
    error = "Language {} is not supported".format(preferred_language)
    print(error)
elif preferred_currency.upper() not in supportedCurrency.values():
    error = "Currency symbol {} is not supported".format(preferred_currency)
    print (error)
else:
    stockprice = StockTrack(stock_symbol, preferred_language, preferred_currency.upper())
    results = stockprice.convertLanguageToPreferred()
    print (results)
