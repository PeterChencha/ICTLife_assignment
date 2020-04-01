class StockTrack(object):
    """Provided a stock symbol find its current price."""
    def __init__(self, symbol):
        super(StockTrack, self).__init__()
        self.symbol = symbol

    def createQuery(self):
        pass

    def processQuery(self):
        pass

    def getPrice(self):
        try:
            if self.symbol == "aapl":
                return 254.29
            else:
                error = "Symbol not found"
                return error
        except Exception as e:
            raise e


input = raw_input ("Enter stock symbol :")
stockprice = StockTrack(input)
results = stockprice.getPrice()
print (results)
