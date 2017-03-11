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

def XLF_true(bond, gs, ms, wfc):
    fair = 3*bond + 2*gs + 3*ms + 2*wfc
    fair = fair/10
    return fair

def buyPackage(bond, gs, ms, wfc):
    buyFair(bond, "BOND", 2011, 3)
    buyFair(gs, "GS", 2012, 2)
    buyFair(ms, "MS", 2013, 3)
    buyFair(wfc, "WFC", 2014, 2)

def sellPackage(bond, gs, ms, wfc):
    sellFair(bond, "BOND", 2011, 3)
    sellFair(gs, "GS", 2012, 2)
    sellFair(ms, "MS", 2013, 3)
    sellFair(wfc, "WFC", 2014, 2)

def tradeBonds(exchange, volume, buy_sell, price, ID):
    write(exchange, {"type": "add", "order_id": ID, "symbol": "BOND", "dir": buy_sell, "price": price, "size": volume})

def buyFair(exchange, fair, item, ID, volume):
    write(exchange, {"type": "add", "order_id": ID, "symbol": item, "dir": "BUY", "price": fair - 1, "size": volume})
    
def sellFair(exchange, fair, item, ID, volume):
    write(exchange, {"type": "add", "order_id": ID, "symbol": item, "dir": "SELL", "price": fair + 1, "size": volume})

def cancel(ID):
    {"type": "cancel", "order_id": ID}
def conversionVALE(exchange, volume,buy_sell):
    write(exchange, {"type": "convert","order_id":1002,"symbol":"VALE", "dir": buy_sell, "size": volume})

def VALTrader(exchange, VALBZ_F, VALE_F,VALBZ_C, VALE_C):
    cancel(999);
    cancel(1000);
    cancel(1003);
    cancel(1004);
    if (VALBZ_F > VALE_F):
        sellFair(exchange, int(VALE_F+(VALBZ_F-VALE_F)/10), "VALBZ", 999, 1)
        buyFair(exchange, int(VALE_F+(VALBZ_F-VALE_F)/10), "VALE", 1000, 1)
    else:
        buyFair(exchange, int(VALBZ_F+9*(VALE_F-VALBZ_F)/10), "VALBZ", 999, 1)
        sellFair(exchange, int(VALBZ_F+9*(VALE_F-VALBZ_F)/10), "VALE", 1000, 1)
    if ( VALE_C == 10):
        conversionVALE(exchange, 10-VALBZ_C,"SELL")
        VALE_C -= 10-VALE_C
        VALBZ_C += 10-VALBZ_C
    elif (VALE_C == -10):
        conversionVALE(exchange, 10+VALBZ_C,"BUY")
        VALE_C += 10+VALBZ_C
        VALBZ_C -= 10+VALBZ_C
    if (VALBZ_C == 10):
        sellFair(exchange, int(VALE_F+(VALBZ_F-VALE_F)/10), "VALBZ", 1003, 9)
    elif (VALBZ_C == -10):
        buyFair(exchange, int(VALBZ_F+9*(VALE_F-VALBZ_F)/10), "VALBZ", 1004, 9)
        



curr_trades = []
EFull = False
BZFull = False
BONDFull = False
GSFull = False
MSFull = False
WFCFull = False
XLFFull = False
xlfTrue = 0
xlfFair = 0
EFair = 0
BZFair = 0
bondFair = 0
gsFair = 0
msFair = 0
wfcFair = 0
xlf_ar = []
valbz = []
vale = []
bond_ar = []
gs_ar = []
ms_ar = []
wfc_ar = []
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

            if ((gsFair != 0) and (msFair !=0) and (wfcFair != 0)):
                xlfTrue = XLF_true(1000, gsFair, msFair, wfcFair)
            if (xlfTrue > xlfFair and (xlfFair != 0) and (xlfTrue != 0)):
                print("GS Fair: ", gsFair, " ", "MS Fair: ", msFair, " ", "WFC Fair: ", wfcFair)
                print("Buying XLF True")
                #sellPackage(1000, gsFair, msFair, wfcFair)
                sellFair(exchange, 1000, "BOND", 2011, 3)
                sellFair(exchange, gsFair, "GS", 2012, 2)
                sellFair(exchange, msFair, "MS", 2013, 3)
                sellFair(exchange, wfcFair, "WFC", 2014, 2)
                buyFair(exchange, xlfTrue, "XLF", 2017, 1)
            else:
                print("GS Fair: ", gsFair, " ", "MS Fair: ", msFair, " ", "WFC Fair: ", wfcFair)
                print("Selling XLF Fair")
                #buyPackage(1000, gsFair, msFair, wfcFair)
                buyFair(exchange,1000, "BOND", 2011, 3)
                buyFair(exchange, gsFair, "GS", 2012, 2)
                buyFair(exchange, msFair, "MS", 2013, 3)
                buyFair(exchange, wfcFair, "WFC", 2014, 2)
                sellFair(exchange, xlfTrue, "XLF", 2018, 1)
            x = time.time()

        feed = read(exchange)
        type = feed['type']
        if (type == "trade"):
            symbol = feed['symbol']
            price = feed['price']
            size = feed['size']


            #Check which symbol we have and update stuff 
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

            elif (symbol == "BOND"):
                if (BONDFull):
                    bond_ar.append(price)
                    bond_ar.pop(0)
                else:
                    if (len(bond_ar) > 5):
                        BONDFull = True
                    bond_ar.append(price)
                bondFair = np.median(bond_ar)

            elif (symbol == "MS"):
                if (MSFull):
                    ms_ar.append(price)
                    ms_ar.pop(0)
                else:
                    if (len(ms_ar) > 5):
                        MSFull = True
                    ms_ar.append(price)
                msFair = np.median(ms_ar)

            elif (symbol == "GS"):
                if (GSFull):
                    gs_ar.append(price)
                    gs_ar.pop(0)
                else:
                    if (len(gs_ar) > 5):
                        GSFull = True
                    gs_ar.append(price)
                gsFair = np.median(gs_ar)

            elif (symbol == "WFC"):
                if (WFCFull):
                    wfc_ar.append(price)
                    wfc_ar.pop(0)
                else:
                    if (len(wfc_ar) > 5):
                        WFCFull = True
                    wfc_ar.append(price)
                wfcFair = np.median(wfc_ar)

            elif (symbol == "XLF"):
                if (XLFFull):
                    xlf_ar.append(price)
                    xlf_ar.pop(0)
                else:
                    if (len(xlf_ar) > 5):
                        XLFFull = True
                    xlf_ar.append(price)
                xlfFair = np.median(xlf_ar)
                print ("XLF Fair updated to: ", xlfFair)
            
            
            VALTrader(exchange, BZFair, EFair,valbz_count, vale_count)



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