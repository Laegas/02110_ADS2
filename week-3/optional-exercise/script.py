# run from cmd as "python script.py < Test01.in"

import sys

x = sys.stdin.readline().replace("\n", "")
y = sys.stdin.readline().replace("\n", "")

def SA(x, y, d):
    M = [ [ None for i in range(len(x)+1) ] for j in range(len(y)+1) ]
    for i in range(len(M)):
        M[i][0] = d*i
    for i in range(len(M[0])):
        M[0][i] = d*i

    for i in range(1, len(M)):
        for j in range(1, len(M[0])):
            M[i][j] = min([penalty(x[j-1], y[i-1]) + M[i-1][j-1], d + M[i-1][j], d + M[i][j-1]])

    row = len(y)
    column = len(x)
    while row > 0 and column > 0:
        toCompare = [M[row-1][column-1], M[row][column-1], M[row-1][column]]
        index = toCompare.index(min(toCompare))
        if index == 0:
            row -= 1
            column -= 1
        elif index == 1:
            column -= 1
            y = y[:column] + '-' + y[column:]
        elif index == 2:
            row -= 1
            x = x[:row] + '-' + x[row:]

    return M[len(M)-1][len(M[0])-1], x, y

def penalty(a, b):
    return 0 if a == b else 1

print("Result", SA(x, y, 1))
