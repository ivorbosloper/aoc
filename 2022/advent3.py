from functools import reduce
from operator import __and__

def value(overlap):
    return 1 + ord(overlap) - (ord('a') if overlap.islower() else ord('A') - 26)

def overlap_summer(it):
    return sum(value(reduce(__and__, map(set, i)).pop()) for i in it)

def f1(input):
    print(overlap_summer([[line[:len(line)//2], line[len(line)//2:]] for line in input]))

def f2(input):
    print(overlap_summer([input[s:s+3] for s in range(0, len(input), 3)]))

# def f1(input):
#     total = 0
#     for line in input:
#         size = len(line)
#         assert size % 2 == 0
#         l1, l2 = line[:size//2], line[size//2:]
#         overlap = (set(l1) & set(l2)).pop()
#         # print(overlap, 1 + ord(overlap) - ord('a' if overlap.islower() else 'A'))
#         total += value(overlap)
#     print(total)

# def f2(input):
#     total = 0
#     for s in range(0, len(input), 3):
#         l = input[s:s+3]
#         overlap = (set(l[0]) & set(l[1]) & set(l[2])).pop()
#         total += value(overlap)
#     print(total)
    
