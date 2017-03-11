#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time



def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.11.90", 20000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

def tradeBonds(exchange, volume, buy_sell, price, ID):
    write(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": buy_sell, "price": price, "size": volume})

if __name__ == "__main__":
    exchange = connect()
    write(exchange, {"type": "hello", "team": "MELDOR"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    buyIndex = 0
    sellIndex = 0
    while(True):
        time.sleep(1)
        tradeBonds(exchange, 1, "BUY", 999, buyIndex)
        ++buyIndex
        tradeBonds(exchange, 1, "SELL", 1001, sellIndex)
        ++sellIndex