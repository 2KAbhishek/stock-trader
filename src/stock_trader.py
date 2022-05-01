import pandas as pd
import yfinance as yf
import random
from tkinter import *
from datetime import datetime
from pandastable import Table
from market import Market
from user import User
from stock import Stock


def pull_data(companies, start_date, end_date):
    '''
    This function pulls data from the yahoo finance API
    Returns:
        stocks - a list of ten Stock objects (10 companies)
    '''
    stocks = []

    for company in companies:
        print("Pulling data for " + company)
        data = yf.download(company, start=start_date, end=end_date)
        value = random.choice(data['Adj Close'])
        stock = Stock(company, value)
        stocks.append(stock)
    return stocks


def refresh_data(df, con, table):
    '''
    Refreshes the stock info on the GUI
    '''
    updated_df = pd.read_sql_query("SELECT * FROM portfolio", con)
    df.update(updated_df)
    table.redraw()


def main():
    '''
    Calls the pull_data() method to upload stock info to the database
    Sets up the GUI window
    '''
    companies = ["AAPL", "IBM", "AMZN", "FB", "NVDA",
                 "TSM", "INTC", "TWTR", "MSFT", "GOOG"]
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 1)
    stocks = pull_data(companies, start_date, end_date)
    user = User(100000)
    # Comment this to make portfolio persistent
    user.clean_portfolio()
    market = Market(stocks, user)

    # Setup table
    for stock in stocks:
        user.add_stock(stock, 0)

    root = Tk()
    root.title("Stock Trader")
    root.geometry("505x300")
    root.resizable(True, True)
    root.configure(background='#FFFFFF')

    frame = Frame(root, bg='#FFFFFF')
    frame.pack(fill=BOTH, expand=True)

    # Read data from sql file
    stocks_df = pd.read_sql_query("SELECT * FROM portfolio", user.user_account)

    print(stocks_df)

    # Create a table
    table = Table(frame, dataframe=stocks_df)
    table.show()

    # Add label for Stock label
    stock_label = Label(frame, text="Stock:", bg='#FFFFFF', fg='#000000')
    stock_label.grid(row=0, column=2)

    # Add a text entry box for the user to enter the stock name
    stock_name = StringVar()
    stock_name_entry = Entry(frame, textvariable=stock_name, width=20)
    stock_name_entry.grid(row=0, column=3)

    # Add label for Quantity label
    quantity_label = Label(frame, text="Quantity:", bg='#FFFFFF', fg='#000000')
    quantity_label.grid(row=1, column=2)

    # Add a text entry box for the user to enter the quantity
    quantity = StringVar()
    quantity_entry = Entry(frame, textvariable=quantity, width=20)
    quantity_entry.grid(row=1, column=3)

    # Add a button to refresh the stock info
    refresh_button = Button(frame, text="Refresh", command=lambda: refresh_data(
        stocks_df, user.user_account, table))
    refresh_button.grid(row=2, column=1)

    # Add a button to buy the stock
    buy_button = Button(frame, text="Buy", command=lambda: market.buy(
        stock_name.get(), int(quantity.get())))
    buy_button.grid(row=2, column=2)

    # Add a button to sell the stock
    sell_button = Button(frame, text="Sell", command=lambda: market.sell(
        stock_name.get(), int(quantity.get())))
    sell_button.grid(row=2, column=3)

    root.mainloop()


if __name__ == "__main__":
    main()
