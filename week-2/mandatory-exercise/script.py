import time

# 50 elements
# ij_loop_counter 1275
# dijx_base_case_counter 1275
# dijx_memoized_counter 12392
# dijx_l_loop_counter 20825
# dijx_if_l_loop_counter 13617

# 100 elements
# ij_loop_counter 5050
# dijx_base_case_counter 5050
# dijx_memoized_counter 101481
# dijx_l_loop_counter 166650
# dijx_if_l_loop_counter 106431

# 5 elements - exponential
# ij_loop_counter 15
# dijx_base_case_counter 15
# dijx_memoized_counter 10
# dijx_l_loop_counter 20
# dijx_if_l_loop_counter 20

# 10 elements - exponential
# ij_loop_counter 55
# dijx_base_case_counter 55
# dijx_memoized_counter 120
# dijx_l_loop_counter 165
# dijx_if_l_loop_counter 165


elements = 40 # 250 takes ~1 second
X = [1]
for i in range(1, elements):
    X.append(X[i-1] + i)

X = [ 2**i for i in range(4)] # exponential sequence
print(X)

D_memoized = None # global var
ij_loop_counter = 0
dijx_base_case_counter = 0
dijx_memoized_counter = 0
dijx_l_loop_counter = 0
dijx_if_l_loop_counter = 0
dijx_total_calls = 0

def max_total_score_for_inflating_sequence(X):
    n = len(X)
    global D_memoized
    global ij_loop_counter
    D_memoized = [ [ None for y in range(n)] for x in range(n)]

    max_score = 0

    for i in range(n):
        for j in range(i, n):
            ij_loop_counter += 1
            temp = D(i,j,X)
            max_score = temp if temp > max_score else max_score

    return max_score

def D(i,j,X):
    global dijx_base_case_counter
    global dijx_memoized_counter
    global dijx_l_loop_counter
    global dijx_if_l_loop_counter
    global dijx_total_calls
    dijx_total_calls += 1
    if i==j:
        dijx_base_case_counter += 1
        return 1

    global D_memoized
    if D_memoized[i][j] is not None:
        dijx_memoized_counter += 1
        return D_memoized[i][j]

    temp_max = []
    for l in range(i+1):
        dijx_l_loop_counter += 1
        if X[i] - X[l] < X[j] - X[i]:
            print(X[l],X[i],X[j])
            dijx_if_l_loop_counter += 1
            temp_max.append(D(l,i,X))

    D_memoized[i][j] = 1 + max(temp_max)
    return D_memoized[i][j]

start_time = time.time()
print(max_total_score_for_inflating_sequence(X))
print("method took %s seconds" % (time.time() - start_time))

print("ij_loop_counter", ij_loop_counter)
print("dijx_base_case_counter", dijx_base_case_counter)
print("dijx_memoized_counter", dijx_memoized_counter)
print("dijx_l_loop_counter", dijx_l_loop_counter)
print("dijx_if_l_loop_counter", dijx_if_l_loop_counter)
print("dijx_total_calls", dijx_total_calls)

