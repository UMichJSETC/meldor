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
def conversionVALE(volume,buy_sell):
    write(exchange, {"type": "convert","order_id":1002,"symbol":"VALE", "dir": buy_sell, "size": volume})

def VALTrader(VALBZ_F, VALE_F,VALBZ_C, VALE_C):
    cancel(999);
    cancel(1000);
    if (VALBZ_F > VALE_F):
        sellFair(int(VALE_F+(VALBZ_F-VALE_F)/10), "VALBZ", 999, 1)
        buyFair(int(VALE_F+(VALBZ_F-VALE_F)/10), "VALE", 1000, 1)
    else:
        buyFair(int(VALBZ_F+9*(VALE_F-VALBZ_F)/10), "VALBZ", 999, 1)
        sellFair(int(VALBZ_F+9*(VALE_F-VALBZ_F)/10), "VALE", 1000, 1)
    if ( VALE_C == 10):
        conversionVALE(10-VALBZ_C,"SELL")
    elif (VALE_C == -10):
        conversionVALE(10+VALBZ_C,"BUY")
    if (VALBZ_C == 10):
        sellFair(int(VALE_F+(VALBZ_F-VALE_F)/10), "VALBZ", 999, 9)
    elif (VALBZ_C == -10):
        buyFair(int(VALBZ_F+9*(VALE_F-VALBZ_F)/10), "VALBZ", 999, 1)
        



curr_trades = []
EFull = False
BZFull = False
EFair = 0
BZFair = 0
valbz = []
vale = []
vale_count = 0 
valbz_count = 0
if __name__ == "__main__":
    exchange = connect()
    write(exchange, {"type": "hello", "team": "MELDOR"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    buyIndex = 1
    sellIndex = 2

    x = time.time()
    tradeBonds(exchange, 100, "BUY", 999, buyIndex)
    tradeBonds(exchange, 100, "SELL", 1001, sellIndex)
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
                    if (len(valbz) > 5):
                        BZFull = True
                    valbz.append(price)
                    print ("We did it!")
                BZFair = np.median(valbz)
            elif (symbol == "VALE"):
                if (EFull):
                    vale.append(price)
                    vale.pop(0)
                else:
                    if (len(vale) > 5):
                        EFull = True
                    vale.append(price)
                EFair = np.median(vale)
            
            VALTrader(BZFair, EFair,valbz_count, vale_count)
            if (type == "fill"):
                orderID = feed['order_id']
                symbol = feed['symbol']
                price = feed['price']
                size = feed['size']
                if (symbol == "VALBZ"):
                    valbz_count += size
                elif (symbol == "VALE"):
                    vale_count += size


            print ("Symbol: ", symbol, " ", "Price: ", price, " ", "Volume: ", size)

        hello_from_exchange = read(exchange)
        #print("The exchange replied:", hello_from_exchange, file=sys.stderr)
        hello_from_exchange = read(exchange)
        #print("The exchange replied:", hello_from_exchange, file=sys.stderr)