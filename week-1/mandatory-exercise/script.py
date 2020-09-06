# run from cmd as e.g. "python script.py < Test07.in"

import sys

n = int(sys.stdin.readline())
s = list(map(int, sys.stdin.readline().split()))
b = list(map(int, sys.stdin.readline().split()))

# First attempt - achieves 10 points, not divide and conquer
# for i in range(n):
#     for j in range(i, n):
#         temp = b[j] - s[i] - (j - i) * 100
#         if temp > maximum:
#             maximum = temp

def divide_and_conquer(s, b):
    mid = int(len(s)/2)
    if mid > 1:
        r1 = divide_and_conquer(s[0:mid],b[0:mid])
        r2 = divide_and_conquer(s[mid:len(s)],b[mid:len(s)])
        min_s = min([r1[1] + (len(s) - mid) * 100, r2[1]])
        max_b = max([r1[2], r2[2] - mid * 100])
        maximum = max([r1[0], r2[0], r2[2] - r1[1] - 100])
        return maximum, min_s, max_b
    else:
        maximum = 0
        min_s = 2147483647
        max_b = 0
        for i in range(len(s)):
            temp_min_s = s[i] + (len(s) - 1 - i) * 100
            temp_max_b = b[i] - i * 100
            min_s = temp_min_s if temp_min_s < min_s else min_s
            max_b = temp_max_b if temp_max_b > max_b else max_b
            for j in range(i, len(s)):
                temp = b[j] - s[i] - (j - i) * 100
                if temp > maximum:
                    maximum = temp
        return maximum, min_s, max_b

result = divide_and_conquer(s, b)
print(result[0])
