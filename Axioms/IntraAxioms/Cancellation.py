from Axioms.Utils.IntraInstance import IntraInstance
from Profile import Profile

class Cancellation(IntraInstance):

    def __init__(self, profile):
        super(Cancellation, self).__init__()

        self._profile = profile

    @classmethod
    # for a given profile, create an instance only if it is a canc profile
    def getInstances(cls, profile, goal, reachedBy = set()):
        return {cls(profile)} if profile.isCancellation() else set()

    def _computeSAT(self, SAT):
        return [[SAT.getLiteral(self._profile, x)] for x in self._profile.getAlternatives()]

    def _computeString(self):
        return f'[CANCELLATION] Profile [{self._profile.toString()}] is a perfect tie: all alternatives must win here.'

    # a cancellation instnace is identified only by the profile
    def _computeHashable(self):
        return self._profile