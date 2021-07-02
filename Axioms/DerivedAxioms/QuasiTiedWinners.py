from Axioms.Utils.DerivedInstance import DerivedInstance
from Profile import Profile
from itertools import combinations

class QuasiTiedWinners(DerivedInstance):

    # Implied by PosRes and Cancellation. If a profile P is obtained
    # by raising x from a canc profile, then F(P)={x}
    activators = {'PositiveResponsiveness', 'Cancellation'}

    @classmethod
    # Function that, checks whether there is an x such that:
    # x never loses a majority contest, and wins at least one
    # any other pair of alts ties. Necessary, but NOT sufficient
    # condition for P to be obtained from a cancellation prof. 
    # Used as a filter before doing the other, expensive, check

    def _findWinner(cls, profile):

        # we begin not knowing who could be this winner
        winner = None

        # check every pair of alternatives (once!)
        for x, y in combinations(profile.getAlternatives(), 2):
            # if we have no clue who the winner is:
            if winner is None:
                # if x >(majority)> y, then we hypothesise x is the winner
                prefers_x = sum([count for ballot, count in profile.getTuples() if profile.prefers(ballot, x, y)])
                if prefers_x != (len(profile) / 2):
                    winner = x if prefers_x > (len(profile) / 2) else y

            # if we think we know who the winner is:
            if winner is not None:
                # if winner is neither x nor y, we want them to tie. If this not true, return None (no winner)
                if winner != x and winner != y:
                    prefers_x = sum([count for ballot, count in profile.getTuples() if profile.prefers(ballot, x, y)])
                    if prefers_x != (len(profile) / 2):
                        return None
                else:
                    # if x = winner, loser = y, it must be the case that x wins. Otherwise, return None
                    loser = y if winner == x else x
                    prefers_w = sum([count for ballot, count in profile.getTuples() if profile.prefers(ballot, winner, loser)])
                    if prefers_w < (len(profile) / 2):
                        return None

        # note that we could return None if we never found any winner.
        return winner

    @classmethod
    # axuiliary method to find cancellation profle 
    # try systematically to lower alternative WINNER until we find a canc profile (if there is one!)
    # note: only done if the above necessary conditions are true
    def _tryLoweringAlt(cls, ballots, winner, soFar = []):
        if not ballots:
            pSoFar = Profile(soFar)
            if pSoFar.isCancellation():
                return pSoFar
            else:
                return None

        reference, rest = ballots[0], ballots[1:]

        while True:
            prof = cls._tryLoweringAlt(rest, winner, soFar + [reference])
            if prof is not None:
                return prof

            if reference.index(winner) == len(reference) - 1:
                return None
            else:
                reference = list(reference)
                rank = reference.index(winner)
                reference[rank] = reference[rank + 1]
                reference[rank + 1] = winner
                reference = tuple(reference)


    @classmethod
    # find the base cancellation profile
    def _findCancProfile(cls, profile):
        # necesary condition: try to identify possible winner
        winner = cls._findWinner(profile)
        # not found? sorry!
        if winner is None:
            return None, None
        # found? return the profile and the alt
        else:
            return cls._tryLoweringAlt(list(profile.allBallots()), winner), winner

    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):

        reachedBy_names = {a.axiomName() for a in reachedBy}
        # since this is an "extra", we could only focus on the simple cases (no loss of completeness)
        # also: a cancellation profile can only be even, hence skip the odd profiles (in terms of #voters)
        if (len(profile) % 2 == 0) : # and ('Reinforcement' in reachedBy_names or 'Goal' in reachedBy_names) and not profile.isCancellation() \
            #and ('Neutrality' not in reachedBy_names):
            canc_prof, x = cls._findCancProfile(profile)
            if canc_prof is not None:
                # return instance if found a profile
                return {cls(profile, canc_prof, x)}

        return set()

    def __init__(self, profile, canc_prof, x):
        super(QuasiTiedWinners, self).__init__()

        # our profile, cancellation profile, and raised alt
        self._profile = profile
        self._canc_prof = canc_prof
        self._winner = x

    def _computeSAT(self, SAT):
        # only WINNER can win
        return [[(1 if x == self._winner else -1) * SAT.getLiteral(self._profile, x)] for x in self._profile.getAlternatives()]

    def _computeString(self):
        return f'[POSITIVE RESPONSENESS, CANCELLATION] In profile [{self._profile.toString()}], {self._winner} has been raised from [{self._canc_prof.toString()}],  a Cancellation profile. Thus it must win.'

    def _computeHashable(self):
        return (self._profile, self._canc_prof, self._winner)