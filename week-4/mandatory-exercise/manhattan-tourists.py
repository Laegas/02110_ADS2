# run from cmd as "python manhattan-tourists.py < Test00.in"

import sys

# def pretty_print(M):
#     for i in range(len(M)):
#         for j in range(len(M[0])):
#             print(str(M[i][j] if M[i][j] != None else "N").ljust(3, " "),end="")
#         print()

n = int(sys.stdin.readline().replace("\n", ""))
# print(n)

R = [[int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')] for i in range(n)]
D = [[int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')] for i in range(n-1)]

# print(R)
# print(D)

W=[[None for i in range(n)] for j in range(n)]
W[0][0] = 0

for i in range(1,n):
    W[0][i] = W[0][i-1] + R[0][i-1]
    W[i][0] = W[i-1][0] + D[i-1][0]

for i in range(1,n):
    for j in range(1,n):
        W[i][j] = max([W[i][j-1] + R[i][j-1], W[i-1][j] + D[i-1][j]])

# pretty_print(W)
print(W[n-1][n-1])
