#!/usr/bin/env python3
"""
Python MapReduce Mapper for WordCount.
Reads lines from STDIN, tokenizes words, and emits (word, 1) tab-separated pairs.
"""

import sys
import re

def main():
    for line in sys.stdin:
        # Strip trailing whitespace and convert to lowercase
        line = line.strip()
        if not line:
            continue
        
        # Extract alphanumeric words
        words = re.findall(r'\b[a-zA-Z0-9_]+\b', line.lower())
        for word in words:
            # Emit key-value pair to STDOUT
            sys.stdout.write(f"{word}\t1\n")

if __name__ == "__main__":
    main()
