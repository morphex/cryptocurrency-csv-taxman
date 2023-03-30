#!/usr/bin/python3

import csv, sys

ZERO = Decimal(0)
DEBUG = True

def DEBUG_PRINT(*arguments):
    if DEBUG:
        print(*arguments, file=sys.stderr)

def guess_separator(csv_data_lines, default=","):
    """Returns a guess at what the column separator is in the CSV data."""
    semicolon_count_header = csv_data_lines[0].count(";")
    semicolon_count_data = semicolon_count_header
    comma_count_header = csv_data_lines[0].count(",")
    comma_count_data = comma_count_header
    for line in csv_data_lines[1:]:
        semicolon_count_data += line.count(";")
        comma_count_data += line.count(",")
    if comma_count_data > semicolon_count_data:
        return ","
    if comma_count_data < semicolon_count_data:
        return ";"
    else:
        DEBUG_PRINT("Unable to determine column separator")
        DEBUG_PRINT("Choosing ;")
        return ";"

def guess_date_format(dates):
    """Guess the date format given a set of dates."""
    year_index = month_index = day_index = None
    for date in dates:
        if date.startswith('"') and date.endswith('"'):
            date = date[1:-1]
        date = date.split(" ")[0]
        date = list(map(int, date.split("-")))
        if not year_index:
            if int(date[0]) > 1000:
                year_index = 0
            else:
                year_index = 2
        if year_index == 0:
            if date[1] > 12:
                day_index = 1
                month_index = 2
                break
            elif date[2] > 12:
                day_index = 2
                month_index = 1
                break
        elif year_index == 2:
            if date[1] > 12:
                day_index = 1
                month_index = 0
                break
            elif date[0] > 12:
                day_index = 0
                month_index = 1
                break
    else:
        raise ValueError("Unable to determine date format")
    return year_index, month_index, day_index

def parse_date(date, format):
    """Returns year, month, day of a parsed date. Format is year_index, month_index, day_index."""
    if date.startswith('"') and date.endswith('"'):
        date = date[1:-1]
    date = date.split(" ")[0]
    date_ = date.split("-")
    year, month, day = date_[format[0]], date_[format[1]], date_[format[2]]
    return int(year), int(month), int(day)

def parse_float(value):
    """Parses a float, using either a . or , as the denominator."""
    try:
        return float(value)
    except ValueError:
        return float(value.replace(",", "."))
