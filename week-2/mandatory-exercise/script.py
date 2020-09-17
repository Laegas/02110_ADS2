import time

elements = 1000 # 250 takes ~1 second
X = [1]
for i in range(1, elements):
    X.append(X[i-1] + i)

# X = [ 2**i for i in range(60)] # exponential sequence
print(X)

D_memoized = None # global var

def max_total_score_for_inflating_sequence(X):
    n = len(X)
    global D_memoized
    D_memoized = [ [ None for y in range(n)] for x in range(n)]

    max_score = 0

    for i in range(n):
        for j in range(i, n):
            temp = D(i,j,X)
            max_score = temp if temp > max_score else max_score

    return max_score

def D(i,j,X):
    if i==j:
        return 1

    global D_memoized
    if D_memoized[i][j] is not None:
        return D_memoized[i][j]

    temp_max = []
    for l in range(i+1):
        if X[i] - X[l] < X[j] - X[i]:
            temp_max.append(D(l,i,X))

    D_memoized[i][j] = 1 + max(temp_max)
    return D_memoized[i][j]

start_time = time.time()
print(max_total_score_for_inflating_sequence(X))
print("method took %s seconds" % (time.time() - start_time))
