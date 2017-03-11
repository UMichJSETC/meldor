#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time



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

def parseExchange(exchange):
    feed = read(exchange)
    type = feed['type']
    if (type == "trade"):
        symbol = feed['symbol']
        price = feed['price']
        size = feed['size']
        return symbol, price, size

curr_trades = []
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
        symbol, price, size = parseExchange(exchange)
        print ("Symbol: ", symbol, " ", "Price: ", price, " ", "Volume: ", size)

        hello_from_exchange = read(exchange)
        #print("The exchange replied:", hello_from_exchange, file=sys.stderr)
        hello_from_exchange = read(exchange)
        #print("The exchange replied:", hello_from_exchange, file=sys.stderr)