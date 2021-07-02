# abstract class for instance

# important: recall the distinction between @classmethod and normal methods
# classmethod is at the class level: in our framework, mostly can to construct objects (i.e., to CREATE instances)
# normal methods refer to a concrete object, which refers to a specific axiom-instance

class Instance:

    @classmethod
    def isIntra(cls):
        return False

    @classmethod
    def isInter(cls):
        return False

    @classmethod
    def axiomName(cls):
        return cls.__name__

    # a normative basis is a set of strings (axiom names)
    @classmethod
    def normativeBasis(cls):
        return {cls.axiomName()}

    def __init__(self):
        # lazy construction
        # these things cost time to create,
        # so I create them only if (when) needed
        self._hashable = None
        self._hash = None
        self._cnf = None
        self._string = None

    # creates SAT encoding
    # we only use CNF encodings
    # a clause is a list of non-zero ints
    # a CNF is a list of lists (clauses)
    # SAT is an object that stores the SAT encoding of the problem: (of type SATEncoding)
    # it can map (Profile, Alternative) --> propositioanl variable
    def _computeSAT(self, SAT):
        return [[]]

    # create SAT encoding if it does not exist, otherwise return it
    def getInstanceSAT(self, SAT):

        if self._cnf is None:
            self._cnf = self._computeSAT(SAT)

        return self._cnf

    def _computeString(self):
        return str()

    # create Explanation text if it does not exist, otherwise return it
    def getExplanation(self):
        if self._string is None:
            self._string = self._computeString()

        return self._string

    def _computeHashable(self):
        return None

    # sort of "signature" of an instance, used to distinguish it
    # from other instances
    # axiomName makes it unique between axioms, the hashable thing
    # is supposed to differentiate it between instances of same axiom

    # compute hash if it does not exist
    # I differentiate between hash and hashable because 
    # hash, afaik, is not guaranteed to be unique (it is used
    # for sets, dicts and such)
    def _getHashable(self):
        if self._hashable is None:
            self._hashable = (self.axiomName(), self._computeHashable())

        return self._hashable

    def __eq__(self, OtherInstance):
        return self._getHashable() == OtherInstance._getHashable()

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._getHashable())

        return self._hash
