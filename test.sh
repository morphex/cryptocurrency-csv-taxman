#!/bin/bash

./rates.py ./testdata/USD-NOK.csv -1,-1 -2
./mda.py testdata/USD-NOK.csv -2
