class Market():
    '''
    This method creates a market space for users to buy and sell stocks
    which would update the stocks attribute and user class accordingly
    Attributes:
        stocks - a list of Stock objects
        user - a User object
    '''

    def __init__(self, stocks, user):
        self.stocks = stocks
        self.user = user

    def find_stock(self, name):
        for stock in self.stocks:
            if stock.name == name:
                return stock

    def buy(self, name, quantity):
        '''
        This method allows users to buy individual stocks, would decrease
        the bank_balance of user as well as the quantity attribute of the
        Stock and call the add_stock() method of the User class
        Args:
            name - the stock being bought
            quantity - the quantity of stocks bought
        Side Effects:
            Reduces bank_balance of User accordingly
            Calls the add_stock() method of User class
        '''
        stock = self.find_stock(name)
        self.user.bank_balance -= stock.value * quantity
        print("User Balance After Buy: " + str(self.user.bank_balance))
        self.user.add_stock(stock, quantity)

    def sell(self, name, quantity):
        '''
        This method allows users to sell individual stocks, would increase
        the bank_balance of user as well as the quantity attribute of the
        Stock and call the sell_stock() method of the User class
        Args:
            name - the stock being sold
            quantity - the quantity of stocks sold
        Side Effects:
            Increases bank_balance of User accordingly
            Calls the sell_stock() method of User class
        '''
        stock = self.find_stock(name)
        self.user.bank_balance += stock.value * quantity
        print("User Balance After Sell: " + str(self.user.bank_balance))
        self.user.sell_stock(stock, quantity)
