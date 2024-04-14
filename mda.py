#!/usr/bin/python3

import csv, sys

from decimal import Decimal
from collections import OrderedDict
from datetime import date as Date
from datetime import timedelta

from csv_utilities import get_sorted_lines, parse_float, is_float, find_absolute_index, filter_on_date_range

from utilities import DEBUG_PRINT

def parse_mda_file(filename, date_index=0, start=None, end=None):
    dates = OrderedDict()
    indexes = float_fields = []
    lines, separator = get_sorted_lines(filename, sort_field=date_index,
                                        keep_datetime_objects=True)
    if start and end:
        lines = filter_on_date_range(start, end, lines, date_index=date_index)
    for line in lines:
        date = line[date_index].date()
        values = []
        if not indexes:
            indexes = list(range(len(line)))
            try:
                indexes.remove(find_absolute_index(line, date_index))
            except ValueError:
                print("Can't remove index", (indexes, date_index))
                raise
        if not float_fields:
            for index in indexes:
                if is_float(line[index]):
                    float_fields.append(index)
        for index in float_fields:
            values.append(parse_float(line[index]))
        dates[date] = values
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
        start_end = sys.argv[3]
        start, end = start_end.split(",")
    except (IndexError, ValueError):
        start = end = None
    dates = parse_mda_file(sys.argv[1], date_index=date_index, start=start, end=end)
    count = 0
    values = []
    for value in list(dates.items())[0][1]:
        values.append(Decimal(0.0))
    for date, value in dates.items():
        if count == 0:
            print(date)
        count += 1
        for index in range(len(values)):
            values[index] += value[index]
    else:
        print(date)
    print("A total of %i columns" % count)
    for value in values:
        print(value / count, )
    print(values)

if __name__ == "__main__":
    runner()
