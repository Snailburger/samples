# -*- coding: utf-8 -*-

""" Internet data handling """

__author__ = "Lars Schneckenburger"
__credits__ = "Lars Schneckenburger"
__version__ = "1.0"
__created__ = "08.04.2021"


import requests
import json
import random
import time

url = "http://160.85.252.148"

class InternetData():

    def __init__(self):
        pass

    def get(self, retries = 5, backoff_in_seconds = 1.5):
        """
        Receive the content of url, parse it as JSON and return the object.
    
        Returns
        -------
        dict
        """
        x = 0
        print("Load Data...\n")
        while True:
            try:
                response = requests.get(url)
                data = response.json()
                return data
            except:
                if x == retries - 1:
                    print(f"Coudn't reach url in {retries} retries")
                    return {}
                else:
                    assert 0 < backoff_in_seconds
                    sleep = (backoff_in_seconds ** x + random.uniform(0, 1))
                    time.sleep(sleep)
                    x += 1

    def repair(self, data):
        """
        Parameters
        ----------
        data : dict
            Dict with wrongly encoded umlauts.

        Returns
        -------
        data : dict
            Repaired dict.
        """
        change_key = {}
        for key, value in data.items():
            if not key.isalpha():
                new_key = key.encode("latin-1").decode("utf-8")
                change_key[key] = new_key
        for old, new in change_key.items():
            data[new] = data.pop(old)
        return data

    def show(self, data):
        """
        Parameters
        ----------
        data : dict
            Dict with data for tabular Bom.

        Returns
        -------
        True if done
        """
        total = 0
        for key in sorted(data):
            if type(data[key]) not in (int, float):
                pass
            elif data[key] < 0:
                pass
            else:
                print("{:15} | {:15}".format(key, data[key]))
                total += data[key]
        print("_" * 33)
        print("{:15} | {:15}".format("SUM", total))
        return True


if __name__ == "__main__":

    internet_data = InternetData()
    data = internet_data.get()
    data = internet_data.repair(data)
    internet_data.show(data)

    print("\ndone")
    print("Author: {}".format(__author__))
    print("Credits: {}".format(__credits__))
