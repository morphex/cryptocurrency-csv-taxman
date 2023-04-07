#!/bin/bash

./process_chain.py ../etc.csv 0,3 :: ../ETC-USD.csv 3,2 0 :: ./testdata/USD-NOK.csv -1 -2
