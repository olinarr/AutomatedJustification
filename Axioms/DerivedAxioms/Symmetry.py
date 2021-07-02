from Axioms.Utils.DerivedInstance import DerivedInstance
from Profile import Profile

from Axioms.InterAxioms.Neutrality import Neutrality

class Symmetry(DerivedInstance):

    # derived axiom of neutrality stating that, if some
    # alts are symmetric, in that set, either all or none win

    activators = {'Neutrality'}

    @classmethod
    # given a self mapping, construct the equivalence class of alternatives
    def _getClusters(cls, mapping):

        # idea: loop through alternatives (for x in mapping --> loop through
        # all keys of mapping --> all alts). For each of these, traverse
        # the alts through the mapping until you loop back to x. This is a 
        # class. Then continue from next unseen alt.

        seen = set()
        clusters = set()
        cluster = set()
        for x in mapping:
            if x in seen:
                continue

            while True:
                y = mapping[x]
                cluster.add(x)
                if y in cluster:
                    if len(cluster) > 1:
                        clusters.add(tuple(sorted(cluster)))
                    seen.update(cluster)
                    cluster = set()
                    break
                else:
                    x = y

        return clusters

    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):

        I = set()

        # since this is an "extra", we could only focus on the simples cases without loss of completeness,
        # that is profile reached by reinforcement or a goal profile, or a profile not reached by neutrality.

        #reachedBy_names = {a.axiomName() for a in reachedBy}
        #if (not reachedBy_names) or ('Reinforcement' in reachedBy_names or 'Goal' in reachedBy_names) and ('Neutrality' not in reachedBy_names):

        # Not active right now.
        if True:

            # we pick a ballot (any) and try to auto-map this profile to itself
            ballots = list(profile.uniqueBallots())
            profile_dict = dict(profile.getTuples())
            # possible improvement: pick the ballot that has the least
            # number of same-count ballots
            reference, rest = ballots[0], ballots[1:]

            for ballot in rest:
                # if they can be mapped, they must have the same counter
                if profile_dict[ballot] == profile_dict[reference]:
                	# try to map... 
                    mapping = {i:j for i, j in zip(reference, ballot)}
                    new_profile_dict = {}
                    for b, c in profile_dict.items():
                        new_ballot = tuple(mapping[i] for i in b)
                        new_profile_dict[new_ballot] = c

                    # Ok, I succesfully auto-mapped
                    if new_profile_dict == profile_dict:
                    	# a cluster is a set of alternatives such that, by symmetry,
                    	# if one wins then all do 
                    	# basically the connected components of the mapping (cycles)
                        clusters = cls._getClusters(mapping)
                        I.add(cls(profile, clusters))

        return I

    def __init__(self, profile, clusters):
        super(Symmetry, self).__init__()

        self._profile = profile
        # frozenset for hashing purposes
        self._clusters = frozenset(clusters)

    def _computeSAT(self, SAT):
        cnf = []

        # for each cluster {x1...xj}, add a clause that says: 
        # x1->...->xj->x1 (so if one wins, they all do)
        for cluster in self._clusters:
        	# a cluster is a tuple
            for i in range(len(cluster)-1):
                cnf.append([-SAT.getLiteral(self._profile, cluster[i]), SAT.getLiteral(self._profile, cluster[i+1])])

            # also, last implies first
            cnf.append([-SAT.getLiteral(self._profile, cluster[-1]), SAT.getLiteral(self._profile, cluster[0])])

        return cnf

    def _computeString(self):
        if len(self._clusters) > 1:
            return f"[NEUTRALITY] Profile [{self._profile.toString()}] is self-connected through neutrality. For each cluster C in {', '.join(map(lambda x: str(set(x)), self._clusters))}, either all elements of C win or they all lose."
        else:
            return f"[NEUTRALITY] Profile [{self._profile.toString()}] is self-connected through neutrality. Either all elements of C={', '.join(map(lambda x: str(set(x)), self._clusters))} win or they all lose."

    def _computeHashable(self):
        return (self._profile, self._clusters)