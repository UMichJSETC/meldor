#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
def tradeBonds(volume, buy_sell, price, ID):
    order = "ADD "
    order += ID
    order += " BOND"
    order += buy_sell
    order += " "
    order += price
    order += " "
    order += volume

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.11.90", 25000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

if __name__ == "__main__":
    exchange = connect()
    write(exchange, {"type": "hello", "team": "MELDOR"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    buyIndex = 0
    sellIndex = 0
    while(True):
        tradeBonds(1, "BUY", 99, buyIndex)
        ++buyIndex
        tradeBonds(1, "SELL", 101, sellIndex)
        ++sellIndex