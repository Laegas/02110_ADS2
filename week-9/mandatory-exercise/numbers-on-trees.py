# run from terminal as "python numbers-on-trees.py < test01.in"
import sys

class FenwickTree:
    def __init__(self, n):
        self.ft = [0] * (n + 1)

    def update(self, i, value):
        while i < len(self.ft) - 1:
            self.ft[i] += value
            i += i & -i

    def get_sum(self, i):
        ans = 0
        while i > 0:
            ans += self.ft[i]
            i -= i & -i
        return ans

if __name__ == '__main__':
    n, m = [int(s) for s in sys.stdin.readline().split()]
    ft = FenwickTree(n)

    for _ in range(m):
        t = int(sys.stdin.readline())
        ft.update(t, 1)
        print(ft.get_sum(t-1))
