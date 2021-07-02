# This file contains various tools to iterate through the implemented axioms.

# Intraprofile
from Axioms.IntraAxioms.AtLeastOne import AtLeastOne
from Axioms.IntraAxioms.Pareto import Pareto
from Axioms.IntraAxioms.Faithfulness import Faithfulness
from Axioms.IntraAxioms.Cancellation import Cancellation
from Axioms.IntraAxioms.Condorcet import Condorcet

intraAxioms_set = {AtLeastOne, Faithfulness, Pareto, Cancellation, Condorcet}

# Interprofile
from Axioms.InterAxioms.Reinforcement import Reinforcement
from Axioms.InterAxioms.PositiveResponsiveness import PositiveResponsiveness
from Axioms.InterAxioms.Neutrality import Neutrality

interAxioms_set = {Reinforcement, Neutrality, PositiveResponsiveness}

# Derived Axioms
from Axioms.DerivedAxioms.Symmetry import Symmetry
from Axioms.DerivedAxioms.QuasiTiedWinners import QuasiTiedWinners
from Axioms.DerivedAxioms.QuasiTiedLosers import QuasiTiedLosers

derived_axiom_set = {Symmetry, QuasiTiedWinners, QuasiTiedLosers}

# General loop function. Not supposed to be used by the user.
# axioms_to_use --> set (or list) of axiom names you want to use
# source --> source iterator
def _loop(axioms_to_use = None, source = None):
    for a in source:
        if a.axiomName() in axioms_to_use:
            yield a

# given a derived axiom h, h.isActive(axioms_to_use) 
# checks whether the axioms in axioms_to_use imply h
def derived_axioms(axioms_to_use = None):
    for h in derived_axiom_set:
        if h.isActive(axioms_to_use):
            yield h

# We loop through intraprofile axioms. always add AtLeastOne!
def intraAxioms(axioms_to_use = None):
    for a in _loop(axioms_to_use + ['AtLeastOne'], intraAxioms_set):
        yield a

# We loop through interprofile axioms. 
def interAxioms(axioms_to_use = None):
    return _loop(axioms_to_use, interAxioms_set)