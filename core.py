# This file contains the main "engine" of the code.

from SATEncoding import SATEncoding
import pylgl
from GraphGen import GraphGen
from time import time

def getSATFromInstances(instances, profiles, alternatives):
    """ instances is a set of objects of type Instance. Similarly for profiles.
    alternatives is a set of alternatives.
    Returns a SATEncoding object, capable of handling various SAT-related tasks.
    Returns also a dictionary to map from an instance (abstract object) to the
    corresponding clauses (concrete encoding)."""

    # Returns the SAT-encoding object. This method accepts the set of profiles and the alternatives, and
    # returns an object capable of handling various SAT related tasks. When created, this object
    # contains a mapping from (profile, alternative) to propositional_variable.
    SAT = SATEncoding(profiles, alternatives)

    # init data structures
    instance2clauses = {}
    explanations = {}

    # for every instance that is not the goal, 
    # obtain the SAT encoding for the instance, and link
    # it to this instance in the mapping. Note that we need to pass
    # the SAT object, as instances need to know the propositional variable
    # corresponding to each (profile, alternative) to make the mapping.
    # The mapping serves to remember, for each clause, the corresponding instance
    for instance in instances:
        if instance.axiomName() != 'Goal':
            instance2clauses[instance] = instance.getInstanceSAT(SAT)
        else:
            # we do not add the goal profile for now; it will be added later on by itself.
            instance2clauses[instance] = []

    return instance2clauses, SAT

def createSAT(goal_profile, axioms_to_use, depth):
    """ Create SAT encoding of the problem. Needs the goal profile, the axioms to use and the maximum depth."""
    # Get the instance graph: instances and profiles.
    instances, profiles = GraphGen(goal_profile, axioms_to_use, depth)
    # encode the instances as SAT.
    instance2clauses, SAT = getSATFromInstances(instances, profiles, goal_profile.getAlternatives())
    # return the mapping instance->clauses, the SAT object, and some data about the length (used to check for fixed point)
    return instance2clauses, SAT, len(instances), len(profiles)

def solveSAT(SAT, outcomesToCheck, instance2clauses, depth, limit):

    """ Find gMUSes of the SAT encoding. Inputs:
    SAT is an object capable of handling various SAT-related tasks.
    outcomesToCheck: set of sets of alterantives. This are the outcomes we try to justify.
    instance2clauses. Mapping from Instance object to its SAT encoding.
    depth. Maximum depth we're looking for. Here just for printing purposes.
    limit. Number of gMUSes to generate. """

    # init structure
    answers = set()
    cnf = []

    # we turn this to a huge cnf formula!
    # loop over all instances. For the goal instance,
    # we keep it apart (we add it later)
    for inst, clauses in instance2clauses.items():
        if inst.axiomName() == 'Goal':
            goal_instance = inst
        else:
            cnf += clauses

    # for every outcome to check...
    for goal_outcome in outcomesToCheck:
        # add goal clause FOR THIS PARTICULAR OUTCOME.
        goal_clauses = goal_instance.getInstanceSAT(SAT, goal_outcome)
        cnf_with_goal = cnf + goal_clauses
        # set it in the mapping as well.
        instance2clauses[goal_instance] = goal_clauses

        # if this set is unsolvable, we might find some justifications, otherwise no.
        if pylgl.solve(cnf_with_goal) == 'UNSAT':

            print(f" A proof for outcome {set(goal_outcome)} exists! Extracting...", flush = True)

            # try extract justification using the SAT object
            normative, explanation = SAT.getJustification(instance2clauses, limit)

            # if we found one: (might be none if normative is nontrivial)
            # make a nice message stating it
            if explanation is not None:                

                size = len(explanation)

                if depth is None:
                    message = f"#### EXPLANATION OF SIZE {size} FOUND ####"
                else:
                    message = f"#### EXPLANATION OF SIZE {size} AND DEPTH {depth} FOUND ####"

                answer = message + "\n"
                answer += "\t* " + "\n\t* ".join(explanation) + "\n"
                answer += ''.join(['#']*len(message))+ "\n\n"

                # answers object records: the nice message, normative basis, the outcome, and size (# of explns)
                answers.add((answer, frozenset(normative), frozenset(goal_outcome), size))
    
    return answers

# main wrapper of this method
# needs: goal profile, outcomes we want to check, axioms to use, maximum depth, verbose (print stuff or not), limit (# of gMUSes to gen)
def iterjustify(goal_profile, outcomesToCheck, axioms_to_use, MAX_DEPTH, verbose = True, limit = 1):

    # init stuff
    outcome, normative, answer, size = None, None, None, None

    # we start from depth 0, and then iteratively increase.
    depth = 0

    # used to check for fixed point. We record always the 
    # size of generated stuff in the previous step, and if it is
    # equalt to the current one, we quit.
    LAST_SEEN_INSTANCES, LAST_SEEN_PROFILES = -1, -1

    # main loop
    while True:

        # if we are not out of max depth yet... (None ---> no bound)
        if MAX_DEPTH is not None and depth > MAX_DEPTH:
            break

        if verbose:
            print(f"Generating code for depth {depth}...", end = ' ', flush = True)
        start = time()
        # create the SAT encoding up to depth depth
        instance2clauses, SAT, seen_instances, seen_profiles = createSAT(goal_profile, axioms_to_use, depth)
        gen_time = time() - start

        # if we found a fixed point, exit
        if LAST_SEEN_INSTANCES == seen_instances and LAST_SEEN_PROFILES == seen_profiles:
            if verbose:
                print("Fixed point of instances found. Quitting...")
            break

        if verbose:            
            print(f"Done: found {seen_instances} instances and {seen_profiles} profiles. Solving...", end = '', flush = True)
        start = time()
        # find justifications (or at least try)
        answers = solveSAT(SAT, outcomesToCheck, instance2clauses, depth, limit)
        sol_time = time() - start

        # if we found some, we're done (we care about at least 1 justification)
        if answers:
            if verbose:
                print('\n')
            break
        else:
            if verbose:
                print(" No justification found.")

        # set this data, for check of fixed point in generation. Augment depth!
        LAST_SEEN_INSTANCES, LAST_SEEN_PROFILES = seen_instances, seen_profiles
        depth += 1

    # return justifications, depth we got to, and time information
    return answers, depth, gen_time, sol_time