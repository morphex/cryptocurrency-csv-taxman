#!/usr/bin/python3

from decimal import Decimal
from datetime import datetime
import csv, sys

ZERO = Decimal(0)
DEBUG = False

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

def guess_time_format(times):
    return 0, 1, 2

def guess_datetime_format(datetimes):
    """Guesses the datetime format, based on a list of datetimes."""
    datetimes = tuple(datetimes)
    whitespace_separator = False
    colon_separator = False
    separator = ""
    for datetime_ in datetimes:
        if " " in datetime_:
            whitespace_separator = True
            separator = " "
            continue
        else:
            if whitespace_separator:
                raise ValueError("Datetimes with and without space separator")
            else:
                colon_separator = True
                separator = ":"
                raise NotImplementedError(": not supported as separator between date and time")
    dates = []
    times = []
    for datetime_ in datetimes:
        date_, time_ = datetime_.split(separator)
        dates.append(date_)
        times.append(time_)
    date_format = guess_date_format(dates)
    time_format = guess_time_format(times)
    return date_format, time_format, separator

def parse_date(date, format):
    """Returns year, month, day of a parsed date. Format is year_index, month_index, day_index."""
    if date.startswith('"') and date.endswith('"'):
        date = date[1:-1]
    date = date.split(" ")[0]
    date_ = date.split("-")
    year, month, day = date_[format[0]], date_[format[1]], date_[format[2]]
    return int(year), int(month), int(day)

def parse_time(time_, format=":"):
    """Returns hour, minute, second of a parsed time."""
    try:
        hour, minute, second = time_.split(format)
    except ValueError:
        hour, minute = time_.split(format)
        second = "00"
    return int(hour), int(minute), int(second)

def parse_float(value):
    """Parses a float, using either a . or , as the denominator."""
    try:
        return float(value)
    except ValueError:
        return float(value.replace(",", "."))

def to_strptime(date_format, time_format, separator):
    """Creates a string to parse dates using strptime."""
    date_ = [None, None, None]
    date_[date_format[0]] = "%Y"
    date_[date_format[1]] = "%m"
    date_[date_format[2]] = "%d"
    time_ = [None, None, None]
    time_[time_format[0]] = "%H"
    time_[time_format[1]] = "%M"
    time_[time_format[2]] = "%S"
    strptime = "%s-%s-%s%s%s:%s:%s" % (date_[0], date_[1], date_[2], separator,
                                   time_[0], time_[1], time_[2])
    return strptime

def sort_lines(csv_lines, datetime_=True, field=0, keep_datetime_objects=False):
    """Sorts CSV lines based on a field."""
    separator = guess_separator(csv_lines)
    for index in range(len(csv_lines)):
        csv_lines[index] = csv_lines[index].split(separator)
    if datetime_:
        date_format, time_format, datetime_separator = \
          guess_datetime_format(map(lambda x: x[field], csv_lines))
        strptime_format = to_strptime(date_format, time_format, datetime_separator)
        DEBUG_PRINT("strptime_format", strptime_format)
        for index in range(len(csv_lines)):
            csv_lines[index][field] = datetime.strptime(csv_lines[index][field],
                                                        strptime_format)
    csv_lines.sort(key=lambda x: x[field])
    if not keep_datetime_objects:
        for index in range(len(csv_lines)):
            csv_lines[index][field] = csv_lines[index][field].strftime(strptime_format)
    return separator

def print_sort_lines(file):
    lines = []
    for line in open(file).readlines():
        lines.append(line.rstrip())
    separator = sort_lines(lines)
    for line in lines:
        print(separator.join(line))

if __name__ == "__main__":
    print_sort_lines(sys.argv[1])
