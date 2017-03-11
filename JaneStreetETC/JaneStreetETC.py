from __future__ import division
import numpy as np
import scipy as sp



def tradeBonds(volume, buy_sell, price):
    order = "ADD "
    order += 5
    order += " BOND"
    order += buy_sell
    order += " "
    order += price
    order += " "
    order += volume