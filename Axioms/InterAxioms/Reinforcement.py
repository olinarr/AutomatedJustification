from Axioms.Utils.InterInstance import InterInstance
from Helpers import bin_partitions
from itertools import permutations
from Profile import Profile

class Reinforcement(InterInstance):

    def __init__(self, p, p1, p2):
        super(Reinforcement, self).__init__()

        # superprofile
        self._profile = p
        # subprofiles. Why sorted? To avoid repetitions (i.e., p=p1+p2 and p=p2+p1 are the same instance)
        self._part1, self._part2 = sorted((p1, p2))

    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):

        # will contain tuples of form (profile, instance)
        P = set()

        ## PART ONE: instance where "profile" is the superprofile.
        if len(profile) > 1:
            # all possible partitions of the ballots
            # notice we enumerate them, so every ballot has an unique id (i, ballot)
            for first, second in bin_partitions(enumerate(profile.allBallots())):

                # take only the ballots
                first = [b for i, b in first]
                second = [b for i, b in second]

                # construct the profiles
                first_profile, second_profile = Profile(first), Profile(second)

                # get instance
                inst = cls(profile, first_profile, second_profile)

                P.add((first_profile, inst))
                P.add((second_profile, inst))

        ## PART TWO: instance where "profile" is a subprofile.

        # other way around: we have a subprofile, get all the superprofiles
        # within the limit of voters of the goal profile
        if len(profile) < len(goal):
            # We just add one single ballot, though. Why? Because eventually
            # we will reach all superprofiles by adding ballots (and those superprofiles
            # will be partitioned again) by induction

            # so, for each ballot
            for ballot in permutations(profile.getAlternatives()):
                # add it to the profile: this is the superprofile
                # (we create a dictionary ballot -> count, where ballot
                # is a tuple of alternatives. Then, we create a Profile object
                # from this)
                new_profile = dict(profile.getTuples())
                if ballot in new_profile:
                    new_profile[ballot] += 1
                else:
                    new_profile[ballot] = 1

                # sub-profiles: this profie, and the singleton we created
                new_profile, singleton = Profile(new_profile), Profile({ballot: 1})

                # instance of the new profile, the profile and the singleton ballot added
                inst = cls(new_profile, profile, singleton)

                P.add((new_profile, inst))
                P.add((singleton, inst))

        return P


    def _computeSAT(self, SAT):
        cnf = []

        # This CNF It's kinda hard to see... For all alternatives,
        for x in self._profile.getAlternatives():
            # literal: x wins in superprofile
            literal = SAT.getLiteral(self._profile, x)        
            # if x loses in superprofiles, then it loses in either of the subprofiles. Note that
            # -literal -> (-... OR -...) can be written as literal OR -... -...
            cnf.append([-SAT.getLiteral(self._part1, x), -SAT.getLiteral(self._part2, x), literal])

            # Furthermore, for all other alternatives y,
            # it holds that
            for y in self._profile.getAlternatives():
                if x != y:
                    # if x wins in superprofile, then: either y loses in a subprofile or x wins in part1.
                    # if x wins in superprofile, then: either y loses in a subprofile or x wins in part2.
                    # since these must hold both, it's basically saying that if x wins, then it must either win in both x or 
                    # that the intersection is empty
                    cnf.append([-literal, SAT.getLiteral(self._part1, x), -SAT.getLiteral(self._part1, y), -SAT.getLiteral(self._part2, y)])
                    cnf.append([-literal, SAT.getLiteral(self._part2, x), -SAT.getLiteral(self._part1, y), -SAT.getLiteral(self._part2, y)])

        return cnf

    def _computeString(self):
        return \
        f'[REINFORCEMENT] Profiles [{self._part1.toString()}] and [{self._part2.toString()}] are disjoint. Thus, if the intersection of F([{self._part1.toString()}]) and F([{self._part2.toString()}]) is non-empty, it must be equal to F([{self._profile.toString()}]).'

    def _computeHashable(self):
        # instance is identified by super, subprofile1 and subprofile2
        # note that we sort p1 and p2 when creating the instance, hence
        # we do not distinguish beween profile, p1, p2 and profile, p2, p1.
        return self._profile, self._part1, self._part2