# Profile object

from collections import Counter
from itertools import permutations, product
from Helpers import sum_to_n, powerset
from itertools import combinations
from math import factorial
from random import choice, randint
from scipy.special import binom

class Profile():

    # read a profile from string
    # syntax: either "210,012,012" or "1:210,2:012" for {#1:2>1>0, #2:0>1>2}
    @classmethod
    def fromString(cls, string):
        if ':' in string:
            profile = {}
            for b in string.split(','):
                if ':' in b:
                    c, b = b.split(':')
                    profile[tuple(int(x) for x in b)] = int(c)
                else:
                    profile[tuple(int(x) for x in b)] = 1

            return cls(profile)
        else:
            ballots = string.split(',')
            return cls(map(lambda b: tuple(int(x) for x in b), ballots))

    ### NEXT FOUR METHODS:
    # generate randomly all profiles with n voters and m alterantives

    @classmethod
    def _aux_iterate(cls, n, m):
        
        # these are already tuples
        ballots = {p for p in permutations(range(m))}

        if n == 1:
            return [Counter((ballot,)) for ballot in ballots]
        else:

            result = []

            for partial in cls._aux_iterate(n-1, m):
                for ballot in ballots:
                    new = Counter(partial)
                    new.update((ballot,))
                    result.append(new)

            return result

    @classmethod
    def _get_iterateAllProfilesInElectorate(cls, n, m):
        res = set()
        for p in cls._aux_iterate(n, m):
            extended_prof = []
            for b, c in p.items():
                for _ in range(c):
                    extended_prof.append(b)

            res.add(tuple(sorted(extended_prof)))

        return res

    @classmethod
    def iterateAllProfilesInElectorate(cls, n, m):
        for p in cls._get_iterateAllProfilesInElectorate(n, m):
            yield cls(p)
                
    @classmethod
    def iterateAllProfiles(cls, n, m):
        for electorate in range(1, n+1):
            for p in cls._get_iterateAllProfilesInElectorate(electorate, m):
                yield cls(p)
    
    ####

    # deprecated
    @classmethod
    def fromName(cls, name):
        profile = {}
        for preference in name[1:].split('s'):
            voter, ballot = preference.split('v')
            profile[int(voter)] = tuple(map(int, ballot))

        return cls(profile)

    # randomly generate from polya urn model
    # a --> alpha 
    @classmethod
    def polyaUrn(cls, n, m, a):
        # possible orders
        orders = list(permutations(range(m)))
        nOrders = len(orders)

        # generate votes
        votes = []
        for _ in range(n):
            vote = choice(orders)
            votes.append(vote)
            orders += round(a * nOrders) * [vote]

        return cls(votes)

    @classmethod
    def _auxWalsh(cls, lb, ub):
        # auxiliary method to gen. singlepeaked a là Toby Walsh
        if lb == ub:
            return (lb,)
        else:
            if randint(0, 1) == 0:
                return cls._auxWalsh(lb+1, ub) + (lb,)
            else:
                return cls._auxWalsh(lb, ub-1) + (ub,)

    @classmethod
    def walshSinglePeaked(cls, n, m):
        # Thanks to Toby Walsh!
        return cls([cls._auxWalsh(0, m-1) for _ in range(n)])

    @classmethod
    def conitzerSinglePeaked(cls, n, m):
        # Thanks Vincent Conitzer!
        # Generates a singlepeaked profile
        profile = []
        for i in range(n):
            top = randint(0, m-1)
            ballot = [top]
            for j in range(m-1):
                a, b = min(ballot)-1, max(ballot)+1
                if a < 0:
                    ballot.append(b)
                elif b > m-1:
                    ballot.append(a)
                else:
                    ballot.append(choice((a, b)))
            profile.append(tuple(ballot))

        return cls(profile)

    def __init__(self, profile):

        # profile can either be a dict (ballot->count)
        # or a list of ballots
        # a ballot is a tuple of alternatives
        # e.g. tuple (2, 1, 0) means 2>1>0

        # self._profile ---> map from ballots to counts (of votes)
        # self._length ----> # voters
        # self._A  -----> alts

        if isinstance(profile, dict):
            self._profile = {b:c for b,c in profile.items() if c > 0}
            self._length = sum(profile.values())
            self._A = set(list(profile.keys())[0])
        else:
            self._profile = {}
            self._length = 0
            self._A = None

            for ballot in profile:

                self._length += 1

                # init alternatives
                if self._A is None:
                    self._A = set(ballot)

                if ballot in self._profile:
                    self._profile[ballot] += 1
                else:
                    self._profile[ballot] = 1

        # these values are costly to create; will be created only if needed
        # (lazy evaluation)

        # hash code
        self._hash = None
        # profile to string
        self._string = None
        # all the ballots (with repetitions!)
        self._allBallots = None

    # in this ballot, x > y?
    def prefers(self, ballot, x, y):
        return ballot.index(x) < ballot.index(y)

    # top within alternatives O according to a ballot
    def getTopOf(self, ballot, O):
        top = None
        for x in O:
            if top is None or self.prefers(ballot, x, top):
                top = x

        return top

    # bottom within alternatives O according to a ballot
    def getBottomOf(self, ballot, O):
        bottom = None
        for x in O:
            if bottom is None or self.prefers(ballot, bottom, x):
                bottom = x

        return bottom

    # stringify a ballot
    def _ballotToString(self, ballot):
        return ">".join(map(str, ballot))

    # stringify a profile
    def toString(self):
        # if it does not exist, create it first
        if self._string is None:
            self._string = ", ".join((f"#{c}:"+self._ballotToString(ballot) \
                for ballot, c in sorted(self._profile.items(),)))

        return self._string

    def getCounts(self):
        # get the unique counts (i.e. all numbers of ballots)
        return self._profile.values()

    # top according to ballot
    def top(self, ballot):
        return ballot[0]

    # rank of x in ballot
    def rank(self, ballot, x):
        return ballot.index(x)

    def getAlternatives(self):
        return self._A

    def uniqueBallots(self):
        return self._profile.keys()

    def allBallots(self):
        # if it does not exist, create it first
        if self._allBallots is None:
            self._allBallots = []
            for ballot, count in self._profile.items():
                self._allBallots += [ballot for _ in range(count)]

        # ballots w/ repetitions
        return self._allBallots

    # return list of pairs of form (ballot, count)
    def getTuples(self):
        return self._profile.items()

    # are this profile and profile "other" equivalent, up to neutrality?
    def isNeutralityEq(self, other):

        if len(self) == len(other) and self.getAlternatives() == other.getAlternatives():
            ref_ballot, ref_count = list(self.getTuples())[0]

            for ballot, count in other.getTuples():
                if count == ref_count:
                    self2other = {i:j for i, j in zip(ref_ballot, ballot)}

                    tentative = {}
                    for b, c in self.getTuples():
                        tentative[tuple(self2other[i] for i in b)] = c

                    if Profile(tentative) == other:
                        return True
        
        return False

    # get borda winner
    def getBorda(self):
        scores = {}
        for a in self.getAlternatives():
            scores[a] = 0
            for b, c in self.getTuples():
                scores[a] += c * (len(self.getAlternatives()) - b.index(a) - 1)

        bestscore, winners = float("-inf"), set()
        for a, score in scores.items():
            if score > bestscore:
                bestscore = score
                winners = {a}
            elif score == bestscore:
                winners.add(a)

        return winners

    # get borda order
    def getBordaSWF(self):
        scores = {}
        for a in self.getAlternatives():
            scores[a] = 0
            for b, c in self.getTuples():
                scores[a] += c * (len(self.getAlternatives()) - b.index(a) - 1)

        # get binary relations...
        bin_order = set()
        for x, y in combinations(self.getAlternatives(), 2):
            if scores[x] > scores[y]:
                bin_order.add((x, y))
            elif scores[x] < scores[y]:
                bin_order.add((y, x))
            else:
                bin_order.add((x, y))
                bin_order.add((y, x))

        return bin_order

    # get copeland winner
    def getCopeland(self):
        scores = {a:0 for a in self.getAlternatives()}

        for x, y in combinations(self.getAlternatives(), 2):
            prefers_x = sum(count for b, count in self.getTuples() if self.prefers(b, x, y))
            prefers_y = sum(count for b, count in self.getTuples() if self.prefers(b, y, x))

            if prefers_x > prefers_y:
                scores[x] += 1
            elif prefers_x < prefers_y:
                scores[y] += 1

        bestscore, winners = float("-inf"), set()
        for a, score in scores.items():
            if score > bestscore:
                bestscore = score
                winners = {a}
            elif score == bestscore:
                winners.add(a)

        return winners

    def getMajorityGraph(self):

        MG = set()

        for x, y in combinations(self.getAlternatives(), 2):
            prefers_x = sum(count for b, count in self.getTuples() if self.prefers(b, x, y))
            prefers_y = sum(count for b, count in self.getTuples() if self.prefers(b, y, x))

            if prefers_x > prefers_y:
                MG.add((x, y))
            elif prefers_x < prefers_y:
                MG.add((y, x))

        return MG


    def getPlurality(self):
        scores = {a:0 for a in self.getAlternatives()}

        for b, c in self.getTuples():
            scores[self.top(b)] += c
        
        bestscore, winners = float("-inf"), set()
        for a, score in scores.items():
            if score > bestscore:
                bestscore = score
                winners = {a}
            elif score == bestscore:
                winners.add(a)

        return winners

    def getCondorcet(self):

        for c in self.getAlternatives():
            flag = True
            for x in self.getAlternatives():
                if c != x:
                    prefers_c = sum(count for b, count in self.getTuples() if self.prefers(b, c, x))
                    if prefers_c <= len(self)/2:
                        flag = False
                        break
            if flag:
                return c

        return None

    # has this profile some pareto-dom alternative?
    def hasPareto(self):
        for x in self._A:
            if self.isPareto(x):
                return True

        return False

    # is x pareto dominated?
    def isPareto(self, x):
        for y in self._A:
            if x != y:
                flag = True
                for ballot in self.uniqueBallots():
                    if self.prefers(ballot, x, y):
                        flag = False
                        break
                if flag:
                    return True
        return False

    # does every pair tie in a pairwise comparison?
    def isCancellation(self):
        if len(self) % 2 != 0:
            return False

        for x, y in combinations(self._A, 2):
            prefers_x = sum([count for ballot, count in self.getTuples() if self.prefers(ballot, x, y)])
            if prefers_x != (len(self) / 2):
                return False

        return True

    # is this profile unanimous (w.r.t. some top alternative)?
    def isUnanymous(self):
        winner = None
        for b in self.uniqueBallots():
            if winner is None:
                winner = self.top(b)
            elif winner != self.top(b):
                return False

        return True

    # check if single peaked. Can give a default dim, or check m! all.
    def isSinglePeaked(self, dim = None):

        # check wheter, given a dimension, y is between x and z.
        isGreater = lambda dim, x, y : dim.index(x) < dim.index(y)
        checkOrder = lambda dim, x, y, z: isGreater(dim, x, y) and isGreater(dim, y, z)
        isBetween = lambda dim, x, y, z: checkOrder(dim, x, y, z) or checkOrder(dim, z, y, x)

        # check wheter all ballots satisfy that, for ordered all pairs of alternatives,
        # singlepeakedness holds
        def checkDim(dim):
            for ballot in self.uniqueBallots():
                for x in self.getAlternatives():
                    for y in self.getAlternatives():
                        if isBetween(dim, y, x, self.top(ballot)):
                            if not self.prefers(ballot, x, y):
                                return False
            return True

        # either check the given dimension, or try all
        if dim is None:
            for dim in permutations(self.getAlternatives()):
                if checkDim(dim):
                    return True
            return False
        else:
            return checkDim(dim)

    # has code
    def __hash__(self):
        # if it does not exist, create it first
        if self._hash is None:
            self._hash = hash(frozenset(self._profile.items()))

        return self._hash

    def __len__(self):
        return self._length

    # equal if the mappings are
    def __eq__(self, other):
        return self._profile == other._profile

    def __lt__(self, other):
        # only for technical purposes, i.e. avoiding
        # doubles in loops (when parsing all profiles, only consider
        # each pair once)
        return self.toString() < other.toString()

    # transform a ballot in formal order: set of tuples
    def _preference2binary(self, ballot):
        bin_order = set()
        for i in range(len(ballot)-1):
            for j in range(i+1, len(ballot)):
                bin_order.add((ballot[i], ballot[j]))

        return bin_order

    def _KendallDistanceLinearOrders(self, b1, b2):
        # kendall tau
        # 0.5 |{(x, y) : x R1 y and y R2 x}|
        score = 0
        for x in self.getAlternatives():
            for y in self.getAlternatives():
                if x != y:
                    if self.prefers(b1, x, y) and self.prefers(b2, y, x):
                        score += 1
        return 0.5 * score

    def _KendallDistanceBinaryOrders(self, ord1, ord2):
        ord1_minus_ord2 = {tpl for tpl in ord1 if tpl not in ord2}
        ord2_minus_ord1 = {tpl for tpl in ord2 if tpl not in ord1}

        return 0.5 * (len(ord1_minus_ord2) + len(ord2_minus_ord1))

    def supportDiversityMeasure(self, k = None):
        # from paper: Measuring Diversity of Preferences in a Group (Hashemi, Endriss)

        # default: count support
        if k is None:
            k = len(self.getAlternatives())

        assert k <= len(self.getAlternatives()), "Undefined distance measure for k > m"

        if k < len(self.getAlternatives()):
            raise NotImplementedError()
        else:
            return len(self.uniqueBallots())

    def distanceDiversityMeasure(self, score = 'kendall', aggr = 'sum'):
        # from paper: Measuring Diversity of Preferences in a Group (Hashemi, Endriss)
        # sum all kendals between all voters

        if score == 'kendall':
            score_func = self._KendallDistanceLinearOrders
        else:
            raise NotImplementedError()

        if aggr == 'sum':
            aggr_func = lambda x, y : x+y
        elif aggr == 'max':
            aggr_func = max
        else:
            raise NotImplementedError()

        score = 0
        for b1, b2 in combinations(self.allBallots(), 2):
            new_score = score_func(b1, b2)
            score = aggr_func(score, new_score)

        return score

    def compromiseDiversityMeasure(self, rule = 'borda', aggr = 'sum'):
        
        # from paper: Measuring Diversity of Preferences in a Group (Hashemi, Endriss)
        # difference between each voter and the outcome of some SWF
        # results aggregated by aggr (e.g. sum)

        if rule == 'borda':
            SWF = self.getBordaSWF()
        elif rule == 'MG':
            SWF = self.getMajorityGraph()
        else:
            raise NotImplementedError()

        if aggr == 'sum':
            aggr_func = lambda x, y : x+y
        elif aggr == 'max':
            aggr_func = max
        else:
            raise NotImplementedError()

        score = 0
        for b, c in self.getTuples():
            # get b as binary order
            b = self._preference2binary(b)
            new_score = c * self._KendallDistanceBinaryOrders(SWF, b)
            score = aggr_func(score, new_score)

        return score