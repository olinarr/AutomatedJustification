from Axioms.Utils.InterInstance import InterInstance
from Profile import Profile

class PositiveResponsiveness(InterInstance):

    def __init__(self, base, lifted, raisedAlt):
        super(PositiveResponsiveness, self).__init__()

        # base profile
        self._base = base
        # profile were an alt has been raised
        self._lifted = lifted
        # the alt
        self._raisedAlt = raisedAlt

    @classmethod
    # substitute a given ballot with a new one in a profile
    def _updateProfile(cls, profile, old_ballot, new_ballot):

        # get the profile dict
        p_dict = dict(profile.getTuples())

        # decrease counter of old (zero counters are ignored in profiles)
        p_dict[old_ballot] -= 1
        # increase, or set 1 if new, the other counter
        if new_ballot in p_dict:
            p_dict[new_ballot] += 1
        else:
            p_dict[new_ballot] = 1

        # return the profile
        return Profile(p_dict)

    @classmethod
    def getInstancesAndProfiles(cls, profile, goal, reachedBy = set()):
        P = set()

        # we try to lift/lower each alternative...
        for x in profile.getAlternatives():
            # only for each possible ballot (since only one voter can raise at a time,
            # this is sufficient: no need to raise all voters)
            for b in profile.uniqueBallots():

                # rank (position) of alternative in the ballot
                rank = b.index(x)

                # can we lower it?
                if rank < len(b)-1:
                    # if so, create new ballot by lowering of one step x
                    new_ballot = list(b)
                    new_ballot[rank] = new_ballot[rank+1]
                    new_ballot[rank+1] = x
                    # create new profile with this
                    p = cls._updateProfile(profile, b, tuple(new_ballot))

                    # create instance: base is p, lifted is profile
                    inst = cls(p, profile, x)
                    P.add((p, inst))

                # can we raise it? This is to get the instance in the other direction
                # Similar as above, but other direction
                if rank > 0:
                    new_ballot = list(b)
                    new_ballot[rank] = new_ballot[rank-1]
                    new_ballot[rank-1] = x
                    p = cls._updateProfile(profile, b, tuple(new_ballot))

                    # Order is important here!!
                    inst = cls(profile, p, x)
                    P.add((p, inst))

        return P

    def _computeSAT(self, SAT):
        cnf = []

        A = self._base.getAlternatives()

        # if wins in base, it wins in lifted
        cnf.append([-SAT.getLiteral(self._base, self._raisedAlt), SAT.getLiteral(self._lifted, self._raisedAlt)])
        for a in A:
            if a != self._raisedAlt:
                # if wins in base, nothing else wins in lifted
                cnf.append([-SAT.getLiteral(self._base, self._raisedAlt), -SAT.getLiteral(self._lifted, a)])

        return cnf

    def _computeString(self):
        return \
            f'[POSITIVE RESPONSENESS] In profile [{self._lifted.toString()}] {self._raisedAlt} gained support from profile [{self._base.toString()}]. Thus if {self._raisedAlt} wins in the latter, it must be the only winner in the former.'

    def _computeHashable(self):
        return (self._base, self._lifted, self._raisedAlt)