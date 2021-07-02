from Axioms.Utils.DerivedInstance import DerivedInstance
from Profile import Profile
from itertools import combinations

class QuasiTiedLosers(DerivedInstance):

    # Implied by PosRes and Cancellation. If a profile P is obtained
    # by lowering x from a canc profile, then (x not in F(P))
    activators = {'PositiveResponsiveness', 'Cancellation'}

    # FOR THE IMPLEMENTATION:
    # symmetrical to QuasiTiedWinner. Check that file!

    @classmethod
    def _findLoser(cls, profile):
        loser = None

        for x, y in combinations(profile.getAlternatives(), 2):
            if loser is None:
                prefers_x = sum([count for ballot, count in profile.getTuples() if profile.prefers(ballot, x, y)])
                if prefers_x != (len(profile) / 2):
                    loser = x if prefers_x < (len(profile) / 2) else y
            if loser is not None:
                if loser != x and loser != y:
                    prefers_x = sum([count for ballot, count in profile.getTuples() if profile.prefers(ballot, x, y)])
                    if prefers_x != (len(profile) / 2):
                        return None
                else:
                    winner = y if loser == x else x
                    prefers_w = sum([count for ballot, count in profile.getTuples() if profile.prefers(ballot, winner, loser)])
                    if prefers_w < (len(profile) / 2):
                        return None

        return loser

    @classmethod
    def _tryRaisingAlt(cls, ballots, loser, soFar = []):
        if not ballots:
            pSoFar = Profile(soFar)
            if pSoFar.isCancellation():
                return pSoFar
            else:
                return None

        reference, rest = ballots[0], ballots[1:]

        while True:
            prof = cls._tryRaisingAlt(rest, loser, soFar + [reference])
            if prof is not None:
                return prof

            if reference.index(loser) == 0:
                return None
            else:
                reference = list(reference)
                rank = reference.index(loser)
                reference[rank] = reference[rank - 1]
                reference[rank - 1] = loser
                reference = tuple(reference)

    @classmethod
    def _findCancProfile(cls, profile):
        loser = cls._findLoser(profile)
        if loser is None:
            return None, None
        else:
            return cls._tryRaisingAlt(list(profile.allBallots()), loser), loser


    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):

        reachedBy_names = {a.axiomName() for a in reachedBy}
        # since this is an "extra", I only focus on the simples cases
        if (len(profile) % 2 == 0) and ('Reinforcement' in reachedBy_names or 'Goal' in reachedBy_names) and not profile.isCancellation() \
            and ('Neutrality' not in reachedBy_names):
            canc_prof, x = cls._findCancProfile(profile)
            if canc_prof is not None:
                return {cls(profile, canc_prof, x)}

        return set()

    def __init__(self, profile, canc_prof, x):
        super(QuasiTiedLosers, self).__init__()

        self._profile = profile
        self._canc_prof = canc_prof
        self._loser = x

    def _computeSAT(self, SAT):
        return [[-SAT.getLiteral(self._profile, self._loser)]]

    def _computeString(self):
        return f'[POSITIVE RESPONSENESS, CANCELLATION] In profile [{self._profile.toString()}], {self._loser} has been lowered from [{self._canc_prof.toString()}], a Cancellation profile. Thus it cannot win here.'

    def _computeHashable(self):
        return (self._profile, self._canc_prof, self._loser)