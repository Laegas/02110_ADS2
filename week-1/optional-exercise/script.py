# run from cmd as "python script.py < Test01.in"

import sys

sys.stdin.readline()
integers = list(map(int, sys.stdin.readline().split()))

for i in reversed(integers):
    print(i, end=" ")
