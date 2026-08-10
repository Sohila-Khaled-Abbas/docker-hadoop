#!/usr/bin/env python3
"""
Python MapReduce Reducer for WordCount.
Reads sorted (word, count) pairs from STDIN, sums occurrences per key, and emits aggregated results.
"""

import sys

def main():
    current_word = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            word, count_str = line.split('\t', 1)
            count = int(count_str)
        except ValueError:
            # Skip corrupted / malformed lines
            continue

        # Because Hadoop Streaming sorts keys during the shuffle phase:
        if current_word == word:
            current_count += count
        else:
            if current_word is not None:
                sys.stdout.write(f"{current_word}\t{current_count}\n")
            current_word = word
            current_count = count

    # Emit the last word
    if current_word is not None:
        sys.stdout.write(f"{current_word}\t{current_count}\n")

if __name__ == "__main__":
    main()
