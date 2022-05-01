import sqlite3
import os


class User():
    '''
    This class creates a user account containing the information about
    stocks owned as well as available money
    Attributes:
        portfolio - a dictionary of format (Stock Name: Number of Stocks Owned)
        bank_balance - amount of money in account
        user_account - a SQL database storing the information of the
                        user (portfolio and bank balance)
        cursor - the cursor that interacts with the user_account database
    '''

    def __init__(self, bank_balance=0):
        self.portfolio = {}
        self.bank_balance = bank_balance

        db_path = os.path.join(os.path.dirname(
            __file__), '../data/portfolio.db')
        self.user_account = sqlite3.connect(db_path)
        self.cursor = self.user_account.cursor()
        table = "CREATE TABLE IF NOT EXISTS portfolio" \
                "(Name TEXT PRIMARY KEY, Quantity INTEGER, Value FLOAT)"
        self.cursor.execute(table)
        self.user_account.commit()

        # Get portfolio from database
        self.cursor.execute("SELECT * FROM portfolio")
        for row in self.cursor.fetchall():
            self.portfolio[row[0]] = row[1]

    def add_stock(self, stock, quantity):
        '''
        This method adds to the portfolio according to the given
        parameters and updates the user_account database
        Args:
            stock - the stock object being bought
            quantity - the quantity of stocks bought
        Side Effects:
            Updates the portfolio dictionary with new stocks
            Updates the user_account database with new stocks
            (erase database and refresh with current portfolio)
        '''
        if stock.name in self.portfolio:
            self.portfolio[stock.name] += quantity
            upd_query = "UPDATE portfolio SET Quantity = ? WHERE Name = ?"
            self.cursor.execute(
                upd_query, (self.portfolio[stock.name], stock.name))
        else:
            self.portfolio[stock.name] = quantity
            ins_query = "INSERT INTO portfolio VALUES (?, ?, ?)"
            self.cursor.execute(
                ins_query, (stock.name, quantity, stock.value))

        self.user_account.commit()

    def sell_stock(self, stock, quantity):
        '''
        This method removes from the portfolio according to the
        given parameters and updates the user_account database
        Args:
            stock - the stock object being removed
            quantity - the quantity of stocks sold
        Side Effects:
            Updates the portfolio dictionary with new info
            Updates the user_account database with new info
        '''
        if stock.name in self.portfolio:
            self.portfolio[stock.name] -= quantity
            upd_query = "UPDATE portfolio SET Quantity = ? WHERE Name = ?"
            self.cursor.execute(
                upd_query, (self.portfolio[stock.name], stock.name))
            self.user_account.commit()

    def clean_portfolio(self):
        '''
        This method removes all the stocks from the portfolio
        and updates the user_account database
        Side Effects:
            Updates the portfolio dictionary with new info
            Updates the user_account database with new info
        '''
        self.portfolio = {}
        self.cursor.execute("DELETE FROM portfolio")
        self.user_account.commit()
