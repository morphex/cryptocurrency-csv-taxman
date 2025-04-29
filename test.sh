#!/bin/bash

./rates.py ./testdata/USD-NOK.csv -1,-1 -2
./mda.py testdata/USD-NOK.csv -2 2023-01-01,2023-12-31
./mda.py testdata/EUR-NOK.csv -2 2023-01-01,2023-12-31
./summarize.py testdata/EUR-NOK.csv 14 15
