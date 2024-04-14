#!/bin/bash

./rates.py ./testdata/USD-NOK.csv -1,-1 -2
./mda.py testdata/USD-NOK.csv -2 2022-01-01,2022-12-31
