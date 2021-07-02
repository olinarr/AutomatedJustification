from Axioms.Utils.InterInstance import InterInstance
from Profile import Profile
from itertools import permutations

class Neutrality(InterInstance):

    def __init__(self, base, mapped, mapping):
        super(Neutrality, self).__init__()

        # base: base profile
        # mapped: mapping(base)
        # mapping: Alternatives -> Alternatives permutation
        self._base = base
        self._mapped = mapped
        self._mapping = mapping

    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):

        # will contain tuples of form (profile, instance)
        P = set()

        # if this profile has already been reached by Neutrality, then we do not need to generate anything here
        # (implied instnaces heuristics)
        # to check this: look at the names of the axioms of the instances in reachedby
        # if neutrality is not here, ok, else quit
        if 'Neutrality' not in map(lambda a: a.axiomName(), reachedBy):

            A = profile.getAlternatives()
            true = tuple(A)

            # for all permutations 
            for perm in permutations(true):
                if perm != true:
                    # construct a mapping
                    mapping = {i:j for i, j in zip(true, perm)}

                    new_profile = dict()

                    # construct mapped profile
                    for b, c in profile.getTuples():
                        new_b = tuple(mapping[i] for i in b)
                        new_profile[new_b] = c

                    new_profile = Profile(new_profile)

                    # get the corresponding instance
                    inst = cls(profile, new_profile, mapping)
                    # add thenew profile
                    P.add((new_profile, inst))

        return P

    def _computeSAT(self, SAT):
        cnf = []

        # if x wins in the base profile, mapping(x) must win in mapping(base)
        # and vice versa
        for x, mapped_x in self._mapping.items():
            cnf.append([-SAT.getLiteral(self._base, x), SAT.getLiteral(self._mapped, mapped_x)])
            cnf.append([-SAT.getLiteral(self._mapped, mapped_x), SAT.getLiteral(self._base, x)])

        return cnf

    def _computeString(self):
        return \
            f'[NEUTRALITY] Profiles [{self._base.toString()}] and [{self._mapped.toString()}] are linked by mapping {self._mapping}.'
    
    # an instance of neutrality is identified by the mapping and profiles it regards
    # note: we need to store a dictionary as a frozenset of its tuples (mappings)
    # because dictionaries are not hashable
    def _computeHashable(self):
        mapping_set = frozenset(self._mapping.items())
        return (self._base, self._mapped, mapping_set)