#!/usr/bin/env python3

"""
Implementation of an algorithm for the 2-SUM problem using hash tables.
"""

import argparse

def parse_file(filename):
    with open(filename) as f:
        content = list(f)
    numbers = set()
    for line in content:
        numbers.add(int(line))
    return numbers

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count 2-SUMs between -10000 and 10000")
    parser.add_argument('filename', type=str, help="file containing numbers")
    parser.add_argument('--verbose', action='store_true', help="print additional messages")

    args = parser.parse_args()
    
    numbers = parse_file(args.filename)
    
    count = 0
    
    for target in range(-10000, 10001):
        if args.verbose: print("Checking target:", target)
        for x in numbers:
            if target < target/2 and (target - x) in numbers:
                count += 1
                if args.verbose: print("2-SUM found:", x, "+", target - x, "=", target)
                break
    
    print(count)