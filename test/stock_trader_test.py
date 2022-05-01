import unittest
import yfinance as yf
import random
from datetime import datetime
from src.user import User
from src.market import Market
from src.stock import Stock


class TestStockTrader(unittest.TestCase):
    def get_data(self, companies, start_date, end_date):
        stocks = []

        for company in companies:
            print("Pulling data for " + company)
            data = yf.download(company, start=start_date, end=end_date)
            value = random.choice(data['Adj Close'])
            stock = Stock(company, value)
            stocks.append(stock)
        return stocks

    def setUp(self):
        self.user = User(100000)
        self.user.clean_portfolio()
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2020, 12, 1)
        self.stocks = self.get_data(['IBM'], start_date, end_date)
        self.market = Market(self.stocks, self.user)

    def test_api_pull(self):
        self.assertEqual(len(self.stocks), 1)

    def test_buy(self):
        self.market.buy('IBM', 10)
        self.market.buy('IBM', 10)
        self.assertEqual(self.user.portfolio['IBM'], 20)

    def test_sell(self):
        self.market.buy('IBM', 10)
        self.market.sell('IBM', 5)
        self.assertEqual(self.user.portfolio['IBM'], 5)

    if __name__ == '__main__':
        unittest.main()
