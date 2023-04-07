#!/usr/bin/python3

import sys
from csv_utilities import get_sorted_lines, parse_float
from rates import parse_rate_file, find_best_match

def runner_main():
    calls = [[]]
    for item in sys.argv[1:]:
        if item == "::":
            calls.append([])
        else:
            calls[-1].append(item)
    initial_call = calls.pop(0)
    if len(initial_call) < 2:
        print("Error in syntax")
        sys.exit(1)
    datetime, value = initial_call[1].split(",")
    initial_datetime_index = int(datetime)
    initial_value_index = int(value)
    initial_lines, separator = get_sorted_lines(initial_call[0],
                                                keep_datetime_objects=True)
    for index in range(len(initial_lines)):
        initial_lines[index].append(
            parse_float(
                initial_lines[index][initial_value_index]
            ))

    for call in calls:
        try:
            filename, low_high, date_index = call
        except ValueError:
            filename, low_high = call
            date_index = 0
        try:
            low, high = low_high.split(",")
        except ValueError:
            low = high = low_high
        low, high, date_index = int(low), int(high), int(date_index)
#        print(filename, low, high, date_index)
        rates = parse_rate_file(filename, low, high, date_index=date_index)
        for index in range(len(initial_lines)):
            date = initial_lines[index][initial_datetime_index]
            rate = find_best_match(rates, date.date())
            new_value = initial_lines[index][-1] * rate
            initial_lines[index].append(new_value)
#    print(initial_lines[0])            
    return initial_lines, separator
    
def runner(string_type=type("")):
    lines, separator = runner_main()
    print(lines[0])
    for line in lines:
        new_line = []
        for item in line:
            if type(item) != string_type:
                item = str(item)
            new_line.append(item)
        print(separator.join(new_line))
    
    
if __name__ == "__main__":
    runner()
