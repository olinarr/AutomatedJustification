from Axioms.Utils.Instance import Instance

# Interprofile instance

class InterInstance(Instance):

    @classmethod
    def isInter(cls):
        return True

    # returns set of instances mentioning a profile and the connected profiles
    # precisely: set of tuples (profile, instance) where instance mentions profile
    # why this instead of two sets Profiles, Instances? In this way, we can memorise
    # for each profile how it was reacehd (by which instance.)
    
    # goal is the goal profile, reachedby is a set of instances that reach
    # 'profile'. These two bits of information might be used for heuristics
    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):
    	# set of tuples (Profile, Instance reaching it)
        return set()