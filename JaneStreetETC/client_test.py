#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time
import numpy as np



def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.11.90", 25000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

def tradeBonds(exchange, volume, buy_sell, price, ID):
    write(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": buy_sell, "price": price, "size": volume})

def buyFair(fair, item, ID, volume):
    write(exchange, {"type": "add", "order_id": ID, "symbol": item, "dir": "BUY", "price": fair - 1, "size": volume})
    
def sellFair(fair, item, ID, volume):
    write(exchange, {"type": "add", "order_id": ID, "symbol": item, "dir": "SELL", "price": fair + 1, "size": volume})

def cancel(ID):
    {"type": "cancel", "order_id": ID}

def VALTrader(VALBZ_F, VALE_F):
    cancel(999);
    cancel(1000);
    if (VALBZ_F > VALE_F):
        sellFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALBZ, 999, volume)
        buyFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALE, 1000, volume)
    else:
        buyFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALBZ, 999, volume)
        sellFair(VALE_F+1(VALBZ_F-VALE_F)/10, VALE, 1000, volume)

curr_trades = []
EFull = False
BZFull = False
EFair = 0
BZFair = 0
valbz = []
vale = []
if __name__ == "__main__":
    exchange = connect()
    write(exchange, {"type": "hello", "team": "MELDOR"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    buyIndex = 1
    sellIndex = 2

    x = time.time()
    while(True):
        if (time.time() > (x + 1)):
            tradeBonds(exchange, 1, "BUY", 999, buyIndex)
            buyIndex = buyIndex + 2
            tradeBonds(exchange, 1, "SELL", 1001, sellIndex)
            sellIndex = sellIndex + 2
            x = time.time()
        feed = read(exchange)
        type = feed['type']
        if (type == "trade"):
            symbol = feed['symbol']
            price = feed['price']
            size = feed['size']
            if (symbol == "VALBZ"):
                if (BZFull):
                    valbz.append(price)
                    valbz.pop(0)
                else:
                    valbz.append(price)
                BZFair = np.median(valbz)
            elif (symbol == "VALE"):
                if (EFull):
                    vale.append(price)
                    vale.pop(0)
                else:
                    vale.append(price)
                EFair = np.median(vale)
            

            print ("Symbol: ", symbol, " ", "Price: ", price, " ", "Volume: ", size)

        hello_from_exchange = read(exchange)
        #print("The exchange replied:", hello_from_exchange, file=sys.stderr)
        hello_from_exchange = read(exchange)
        #print("The exchange replied:", hello_from_exchange, file=sys.stderr)