class StockTrack(object):
    """docstring for StockTrack."""
    def __init__(self, symbol):
        super(StockTrack, self).__init__()
        self.symbol = symbol

    def getPrice(self):
        try:
            if self.symbol == "aapl":
                return 254.29
            else:
                error = " Symbol not found"
        except Exception as e:
            raise e


input = raw_input ("Enter stock symbol :")
stockprice = StockTrack(input)
results = stockprice.getPrice()
print (results)
