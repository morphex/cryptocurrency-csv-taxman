#!/usr/bin/python3

import csv, sys

from decimal import Decimal
from collections import OrderedDict
from datetime import date as Date
from datetime import timedelta

from csv_utilities import get_sorted_lines, parse_float
from utilities import DEBUG_PRINT

def parse_rate_file(filename, low, high, date_index=0):
    rates = OrderedDict()
    lines, separator = get_sorted_lines(filename, sort_field=date_index,
                                        keep_datetime_objects=True)
    low_index = int(low)
    high_index = int(high)
    for line in lines:
        date = line[date_index].date()
        low_ = Decimal(parse_float(line[low_index]))
        high_ = Decimal(parse_float(line[high_index]))
        rates[date] = ((low_ + high_) / 2)
    return rates

def find_best_match(rates, date, offset=0):
    """Returns the rate for the matching day, or the first available prior date."""
    DEBUG_PRINT(date, offset)
    if offset < -10:
        raise ValueError("Invalid rates/date", date, offset)
    try:
        return rates[date - timedelta(days=offset)]
    except KeyError:
        return find_best_match(rates, date, offset - 1)

def runner():
    try:
        low_high = sys.argv[2]
    except IndexError:
        print("Error, use:", sys.argv[0], sys.argv[1], "low,high [date index]")
        print()
        print("For example,", sys.argv[0], sys.argv[1], "3,2")
        print("low, high and date index supports python-style indexing, for example 0 or -1")
        sys.exit(1)
    try:
        date_index = int(sys.argv[3])
    except IndexError:
        date_index = 0
        print(sys.argv)
        sys.exit()
    low, high = low_high.split(",")
    low = int(low)
    high = int(high)
    rates = parse_rate_file(sys.argv[1], low, high, date_index=date_index)
    keys = tuple(rates.keys())
    print(keys[0], rates[keys[0]], keys[-1], rates[keys[-1]], len(rates))

if __name__ == "__main__":
    runner()
