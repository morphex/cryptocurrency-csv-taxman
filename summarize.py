#!/usr/bin/python3

import csv, sys

from decimal import Decimal
from collections import OrderedDict
from datetime import date as Date
from datetime import timedelta

from csv_utilities import get_sorted_lines, parse_float, is_float, find_absolute_index, filter_on_date_range, ZERO

from utilities import DEBUG_PRINT

def parse_transaction_file(filename, date_index=0, field=1, operators=""):
    dates = OrderedDict()
    indexes = []
    lines, separator = get_sorted_lines(filename, sort_field=date_index,
                                        keep_datetime_objects=True, expect_quotes=True)
    for line in lines:
        datetime = line[date_index]
        value = parse_float(line[field])
        if value < ZERO and not "subtract" in operators:
            continue
        if value > ZERO and not "add" in operators:
            continue
        dates[datetime] = value
    return dates


def runner():
    try:
        pass
    except IndexError:
        print("Error, use:", sys.argv[0], sys.argv[1], "")
        print()
        print("For example,", sys.argv[0], sys.argv[1], "")
        print("date index supports python-style indexing, for example 0 or -1")
        sys.exit(1)
    try:
        date_index = int(sys.argv[2])
    except IndexError:
        date_index = 0
        print(sys.argv)
        sys.exit()
    try:
        field = sys.argv[3]
        field = int(field)
    except (IndexError, ValueError):
        field = 1
    operators = "add,subtract"
    if "--only-add" in sys.argv[3:]:
        operators = "add"
    elif "--only-subtract" in sys.argv[3:]:
        operators = "subtract"
    operators = operators.split(",")
    transactions = parse_transaction_file(sys.argv[1], date_index=date_index,
                                          field=field, operators=operators)
    count = 0
    values = []
    for date, value in transactions.items():
        print(date, value)
    
if __name__ == "__main__":
    runner()
