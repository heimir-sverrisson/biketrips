#!/usr/bin/env python3
#
# Remove duplicate paths
#
# Heimir Sverrisson, October 2017
#
import csv

def read_all_pairs():
    no_dup = {}
    reader = csv.reader(open('all_pairs.csv', 'r'))
    for row in reader:
        a, b = row
        key = "%d,%d" % (int(a), int(b))
        rev = "%d,%d" % (int(b), int(a))
        if not rev in no_dup:
            no_dup[key] = True
    return no_dup

def main():
    no_dup = read_all_pairs()
    print(len(no_dup))

if __name__ == '__main__':
    main()
