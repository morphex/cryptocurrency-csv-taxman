#!/usr/bin/python3

import sys
from csv_utilities import get_sorted_lines, parse_float, print_csv_lines
from rates import parse_rate_file, find_best_match
from utilities import DEBUG_PRINT

def print_syntax_info():
    print()
    print("The following example takes crypto transactions, converts them to USD, then NOK")
    print()
    print("./process_chain.py ../etc.csv 0,3 :: ../ETC-USD.csv 3,2 :: ./testdata/USD-NOK.csv -1 -2")
    print()
    print("./process_chain.py <CSV file> <date_index,value_index> ::")
    print("                   <CSV file> <low_index,high_index> [date_index, default 0] ::")
    print("                   <CSV file> <low_and_high_index> [date_index, default 0]")
    print()
    print("low_index,high_index can be two fields separated by a comma, or just one field, one number as the example shows.")
    print()
    
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
        print_syntax_info()
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
            try:
                filename, low_high = call
                date_index = 0
            except ValueError:
                print("Error in syntax")
                print_syntax_info()
                sys.exit()
        try:
            low, high = low_high.split(",")
        except ValueError:
            low = high = low_high
        low, high, date_index = int(low), int(high), int(date_index)
        rates = parse_rate_file(filename, low, high, date_index=date_index)
        for index in range(len(initial_lines)):
            date = initial_lines[index][initial_datetime_index]
            rate = find_best_match(rates, date.date())
            new_value = initial_lines[index][-1] * rate
            initial_lines[index].append(new_value)
    return initial_lines, separator

def runner(string_type=type("")):
    lines, separator = runner_main()
    DEBUG_PRINT(lines[0])
    print_csv_lines(lines, separator)
    
if __name__ == "__main__":
    runner()
