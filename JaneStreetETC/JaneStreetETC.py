from __future__ import division
import numpy as np
import scipy as sp



def tradeBonds(volume, buy_sell, price, ID):
    order = "ADD "
    order += ID
    order += " BOND"
    order += buy_sell
    order += " "
    order += price
    order += " "
    order += volume

def VALTrader(VALBZ_F, VALE_F):
    cancel(999);
    cancel(1000);
    if (VALBZ_F > VALE_F):
        sellFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALBZ, 999, volume)
        buyFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALE, 1000, volume)
    else:
        buyFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALBZ, 999, volume)
        sellFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALE, 1000, volume)


if (type == "fill"):
    orderID = feed['order_id']
    symbol = feed['symbol']
    price = feed['price']
    size = feed['size']
    if (symbol == "VALBZ"):
        val_count += size
    elif (symbol == "VALE"):
        val_count += size
