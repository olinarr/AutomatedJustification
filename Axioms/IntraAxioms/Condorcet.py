from Axioms.Utils.IntraInstance import IntraInstance
from Profile import Profile

class Condorcet(IntraInstance):

    def __init__(self, profile, condorcet):
        super(Condorcet, self).__init__()

        self._profile = profile
        self._condorcet = condorcet


    # for a given profile, create an instance only if it has a condorcet winner
    @classmethod
    def getInstances(cls, profile, goal, reachedBy = set()):
        condorcet = profile.getCondorcet()

        return {cls(profile, condorcet)} if condorcet is not None else set()

    def _computeSAT(self, SAT):

        c = self._condorcet
        return [[(1 if x == c else -1) * SAT.getLiteral(self._profile, x)] for x in self._profile.getAlternatives()]

    def _computeString(self):
        return f'[CONDORCET] In profile [{self._profile.toString()}], {self._condorcet} is a Condorcet winner: it must win.'

    # an instance is identified only by the profile.
    def _computeHashable(self):
        return self._profile