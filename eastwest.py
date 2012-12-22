def Count(famno, n, k):
    if famno == 1:
        return binomial(n, k)
    elif famno == 2:
        return StirCyc(n, k)
    elif famno == 3:
        return StirSet(n, k)
    elif famno == 4:
        return CountPartitions(n, k)
    elif famno == 5:
        return CountOrderedPtns(n, k)
    elif famno == 6:
        return CountRuns(n, k)
    else:
        return IntegerPtns(n, k)

def CountCycles(perm):
    c = 0
    pr = -perm
    n = len(pr)
    for i in range(1, n+1):
        if pr[i] < 0:
            c += 1
            pr[i] = -pr[i]
            i0 = i
            i = pr[i]
            while i != i0:
                pr[i] = abs(pr[i])
                i = pr[i]

def CountOrderedPtns(n, k):
    if n < 0 or k < 1:
        return 0
    elif n == 0 or k == 1:
        return 1
    else:
        return CountOrderedPtns(n, k-1) + CountOrderedPtns(n-1, k)

def CountPartitions(n, k):
    if n < 1 or k < 1 or n < k:
        return 0
    elif n == 1:
        return 1
    else:
        return CountPartitions(n-1, k-1) + CountPartitions(n-k, k)

def CountRuns(n, k):
    if n < 1 or k < 1:
        return 0
    elif n < k:
        return 0
    elif n == 1:
        return 1
    else:
        return k*CountRuns(n-1, k) + (n-k+1)*CountRuns(n-1, k-1)

def IntegerPtns(n, k):
    if n < 1 or k < 1 or n < k:
        return 0
    elif n == 1 and k == 1:
        return 1
    else:
        return IntegerPtns(n-1, k-1) + IntegerPtns(n-k, k)

def List(famno, n, k):
    if famno == 1:
        return ListKSubSets(n, k)
    elif famno == 2:
        return ListPermsCycles(n, k)
    elif famno == 3:
        return ListSetPtns(n, k)
    elif famno == 4:
        return PartitionList(n, k)
    elif famno == 5:
        return ListOrderedPtns(n, k)
    elif famno == 6:
        return ListRuns(n, k)
    else:
        return ListIntegerPtns(n, k)

def ListIntegerPtns(n, k):
    # XXX: Should be memoized (original has: "option remember")
    # eastop = y -> applyop(t->t+1, 1, y)
    # westop = (y, j) -> [j, op(y)]
    if n <= 0 or k <= 0 or n < k:
        return []
    elif n == 1:
        return [1]
    else:
        east = ListIntegerPtns(n-1, k-1)
        west = ListIntegerPtns(n-k, k)
        return (op(map, eastop, east), op(map(westop, west, k)))

