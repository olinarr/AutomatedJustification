## various helper functions
from itertools import chain, combinations, permutations
from operator import sub
from scipy.special import binom
from math import factorial

def kPermutations(iterable, k):
    # all permutations of all subsets of k elements of iterable
    for comb in combinations(iterable, k):
        for perm in permutations(comb):
            yield perm

def powerset(iterable):
    # powerset
    # from https://stackoverflow.com/a/41626759/3042497
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def count_profiles(n, m):
    # count all multisets of n voters, m alts
	return int(binom(n+factorial(m)-1, n))

def count_profiles_all(n, m):
    # count all multisets up to n voters (for m alts)
	return sum(count_profiles(k, m) for k in range(1, n+1))

def bin_partitions(A):
    # Algorithm for partitioning in two sets:
    # Fix one element always in one set (so order does not count)
    # loop in the powerset of the rest
    # assign the current subset to the same set with the fixed element, all the rest in the other
    # avoid the case with all the elements in the first set

    # I use this in the Reinforcement axiom

    A = set(A)
    listA = list(A)
    chosen, rest = listA[0], listA[1:]
    for first in map(set, powerset(rest)):
        first.add(chosen)
        if len(first) < len(listA):
            yield (first, A-first)

def sum_to_n(n):
    # from https://stackoverflow.com/a/2065624
    # Generate the series of integer lists which sum to an integer, n.
    # I use this to exhaustively generate all profiles with a certain # of voters, alternatives. See Profile.py
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in combinations(mid, i)) 
    res = (list(map(sub, chain(s, e), chain(b, s))) for s in splits)
    return set(map(tuple, map(sorted, res)))
