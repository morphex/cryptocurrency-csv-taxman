#!/bin/bash

./process_chain.py ../eth.csv 0,3 :: ../ETH-USD.csv 3,2 0 :: ./testdata/USD-NOK.csv -1 -2
