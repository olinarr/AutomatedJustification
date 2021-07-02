from Axioms.Utils.IntraInstance import IntraInstance
from Profile import Profile

class Pareto(IntraInstance):

    def __init__(self, profile, pareto):
        super(Pareto, self).__init__()

        self._profile = profile
        self._pareto = pareto

    @classmethod
    # for every pareto-dom alt, create an instance
    def getInstances(cls, profile, goal, reachedBy = set()):
        I = set()
        nParetos = 0
        for x in profile.getAlternatives():
            if profile.isPareto(x):
                nParetos += 1
                I.add(cls(profile, x))
        
        return I

    # in this profile, the pareto-dom alt must lose.
    def _computeSAT(self, SAT):
        return [[-SAT.getLiteral(self._profile, self._pareto)]]

    def _computeString(self):
        return f'[PARETO] In profile [{self._profile.toString()}], {self._pareto} is Pareto-dominated.'

    # a pareto instance is identified by its profile and alt.
    def _computeHashable(self):
        return self._profile, self._pareto