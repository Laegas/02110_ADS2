import time
import numpy as np

# size of S from the exercise
integers = 10000 # takes 0.3 seconds with the printing which is slow af

s = np.random.randint(low=-10, high=10, size=integers)
memoized = [[None for _ in range(integers)] for _ in range(2)]

def L(b,i,s):
    global memoized
    if memoized[b][i-1] is not None:
        return memoized[b][i-1]
    elif i == 0:
        return 0
    elif b == 1 and i == 1:
        return s[0]
    elif b == 0 and i == 1:
        return -s[0]
    elif b == 1 and i > 1:
        memoized[b][i-1] = max(L(0, i-1, s), L(0, i-2, s) + s[i-2]) + s[i-1]
    elif b == 0 and i > 1:
        memoized[b][i-1] = max(L(1, i-1, s), L(1, i-2, s) - s[i-2]) - s[i-1]
    else:
        raise "WTF, " + str(b) + "; " + str(i)
    return memoized[b][i-1]

start_time = time.time()
for b in range(2):
    for i in range(integers+1):
        print("L(", b, ",", i, ") =", L(b,i,s), end="; ")
    print()
print("method took %s seconds" % (time.time() - start_time))
