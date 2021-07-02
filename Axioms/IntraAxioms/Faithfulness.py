from Axioms.Utils.IntraInstance import IntraInstance
from Profile import Profile

class Faithfulness(IntraInstance):

    def __init__(self, profile):
        super(Faithfulness, self).__init__()

        self._profile = profile
        self._top = profile.top(list(profile.uniqueBallots())[0])

    @classmethod
    # for a given profile, create an instance only if it is a singleton
    def getInstances(cls, profile, goal, reachedBy = set()):
        return {cls(profile)} if len(profile) == 1 else set()

    def _computeSAT(self, SAT):
        return [[(1 if x == self._top else -1) * SAT.getLiteral(self._profile, x)] for x in self._profile.getAlternatives()]

    def _computeString(self):
        return f'[FAITHFULNESS] In profile [{self._profile.toString()}] there is only one voter: thus, {self._top} must win.'

    # an instance is identified only by the profile.
    def _computeHashable(self):
        return self._profile