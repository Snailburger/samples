# -*- coding: utf-8 -*-

""" Currency Converter """

__author__ = "Lars Schneckenburger"
__credits__ = "Lars Schneckenburger"
__version__ = "1.0"
__created__ = "01.04.2021"


import requests
import json

url = "http://www.floatrates.com/daily/chf.json"

class CurrencyConverter():

    __data = {}

    def __init__(self):
        pass

    def __get_data(self):
        """
        Receive the content of url, parse it as JSON and return the object.

        """
        try:
            response = requests.get(url)
            self.__data = response.json()
        except Exception as e:
            print(e)

    def convert_amount(self, from_cur, to_cur, amount):
        """
        Parameters
        ----------
        from_cur : str
            Currency old
        to_cur : str
            Currency new
        amount : float
            Amount in old currency.

        Raises
        ------
        Exception
            Invalid currency(ies).

        Returns
        -------
        amount : float
            Amount in new currency.

        """
        from_cur = from_cur.lower()
        to_cur = to_cur.lower()
        self.__get_data()
        self.__data["chf"] = {'rate': 1}
        if not to_cur in self.__data or not from_cur in self.__data:
            raise Exception("Invalid currency(ies)!")
        amount = amount / self.__data[from_cur]["rate"] * self.__data[to_cur]["rate"]
        assert 0 <= amount
        return amount

    def get_rate(self, cur):
        """
        Parameters
        ----------
        cur : str
            Currency for rate.

        Raises
        ------
        Exception
            Invalid currency.

        Returns
        -------
        rate : float
            CHF:XXX rate for any given currency XXX..

        """
        self.__get_data()
        if not cur in self.__data:
            raise Exception("Invalid currency!")
        rate = self.__data[cur]["rate"]
        return rate


if __name__ == "__main__":

    try:
        x = CurrencyConverter()
        txt = "CHF-USD"
        print("{:10}{:10.2f}".format(txt, x.get_rate("usd"))) # ~10.60
        txt = "10 CHF"
        print("{:10}{:10.2f} USD".format(txt, x.convert_amount("chf", "usd", 10))) # ~10.60
        txt = "10 USD"
        print("{:10}{:10.2f} CHF".format(txt, x.convert_amount("usd", "chf", 10))) # ~ 9.43
        txt = "10 USD"
        print("{:10}{:10.2f} EUR".format(txt, x.convert_amount("usd", "eur", 10))) # ~ 8.47
        x.convert_amount("aad", "eur", 10)
    except Exception as error:
        print(error)

    print("\ndone")
    print("Author: {}".format(__author__))
    print("Credits: {}".format(__credits__))
