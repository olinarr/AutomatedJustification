from Axioms.Utils.Instance import Instance

# Intraprofile instance

class IntraInstance(Instance):

    @classmethod
    def isIntra(cls):
        return True

    # returns instances mentioning a profile. Precisely, a set of instances
    # goal is the goal profile, reachedby is a set of instances that reach
    # 'profile'. These two bits of information might be used for heuristics
    @classmethod
    def getInstances(cls, profile, goal, reachedBy = set()):
        return set()