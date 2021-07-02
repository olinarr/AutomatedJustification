# Abstract class for Derived Axiom Instance

from Axioms.Utils.IntraInstance import IntraInstance

# a derived axiom is an intraprofile axiom
class DerivedInstance(IntraInstance):

    # axioms that imply this axiom
    activators = set()

    @classmethod
    # check whether this derived axiom is implied
    def isActive(cls, corpus):
        return cls.activators.issubset(corpus)

    @classmethod
    # normative basis, in this framework, are represented as
    # sets of axiom names
    # normative basis of this axiom ---> its activators
    def normativeBasis(cls):
        return {str(a) for a in cls.activators}

    def __init__(self):
        super(DerivedInstance, self).__init__()