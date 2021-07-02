from Axioms.Utils.IntraInstance import IntraInstance
from Profile import Profile

# Goal instance
# Sort of a unicum between the intraprofile instances, works
# a little bit differently.

class Goal(IntraInstance):

    # goal instnace just stores the profile, not the outcome
    # why? because, since we might try to justify different outcomes,
    # the outcome is added at SAT-encoding time, later on
    def __init__(self, profile):
        super(Goal, self).__init__()

        self._profile = profile

    # the goal instnace is created explicitly
    @classmethod
    def getInstances(cls, profile, goal, reachedBy = set()):
        Exception("You don't use Goal instances like this. Use __init__!")

    # SAT encode 
    # also needs outcome, as, as we said, we can try different outcomes
    # this CNF says: alts in outcome must win, the others must not.
    def getInstanceSAT(self, SAT, outcome):
        return [[(-1 if x in outcome else 1) * SAT.getLiteral(self._profile, x) for x in self._profile.getAlternatives()]]

    # explanation
    def _computeString(self):
        return f"[GOAL] F([{self._profile.toString()}]) must be equal to the goal outcome."

    # The goal instance is identified only by the profile.
    def _computeHashable(self):
        return self._profile