from Axioms.Utils.IntraInstance import IntraInstance
from Profile import Profile
from itertools import combinations

class AtLeastOne(IntraInstance):

    def __init__(self, profile):
        super(AtLeastOne, self).__init__()

        self._profile = profile

    @classmethod
    # every profile has an instance of this axiom, no check!
    def getInstances(cls, profile, goal, reachedBy = set()):
        return {cls(profile)}

    def _computeSAT(self, SAT):
        return [[SAT.getLiteral(self._profile, x) for x in self._profile.getAlternatives()]]

    def _computeString(self):
        return f'[AT LEAST ONE] In profile [{self._profile.toString()}] at least an alternative must win.'

    def _computeHashable(self):
        return self._profile