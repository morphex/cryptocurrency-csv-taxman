#!/usr/bin/python3

import csv, sys

from decimal import Decimal
from collections import OrderedDict
from datetime import date as Date
from datetime import timedelta

from csv_utilities import get_sorted_lines, parse_float

def parse_rate_file(filename, low, high, skip_header=True):
    rates = OrderedDict()
    lines, separator = get_sorted_lines(filename)
    date_index = 0
    low_index = int(low)
    high_index = int(high)
    for line in lines:
        date = line[date_index]
        low_ = Decimal(parse_float(line[low_index]))
        high_ = Decimal(parse_float(line[high_index]))
        rates[date] = ((low_ + high_) / 2)
    return rates

def runner():
    try:
        low_high = sys.argv[2]
    except IndexError:
        print("Error, use:", sys.argv[0], sys.argv[1], "low,high")
        sys.exit(1)
    low, high = low_high.split(",")
    low = int(low)
    high = int(high)
    rates = parse_rate_file(sys.argv[1], low, high)
    print(rates)

if __name__ == "__main__":
    runner()
