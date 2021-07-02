from collections import deque, defaultdict
from Axioms.Utils.axiomIterator import intraAxioms, interAxioms, derived_axioms
from Axioms.IntraAxioms.Goal import Goal

# Function that, given a goal profile (goal), the axioms, and a maximum depth,
# generate corresponding the instance graph (that is, profiles and instances)
def GraphGen(goal, axioms_to_use, MAX_DEPTH):

    # Goal(profile) ---> Goal instance of the profile
    # The outcome will be specified later on, before encoding
    # the instances as SAT. The reason is that we want to try to
    # justify multiple outcomes.
    goal_instance = Goal(goal)

    # fifo queue used to explore the graph, a là BFS
    fifo = deque()
    # (profile, depth)
    fifo.append((goal, 0))

    # init instances and profiles sets
    I, P = set(), set()
    I.add(goal_instance)

    # used to memorise, for each profile, by which
    # instances it has been reached. Useful to make some heuristics
    reachedBy = defaultdict(set)
    reachedBy[goal].add(goal_instance)
    
    # while the queue is nonempty
    while fifo:
        
        # pop a profile, and its depth
        profile, depth = fifo.popleft()

        # if profile was not explored yet...
        if profile not in P:

            # ...now it is!
            P.add(profile)

            # for every intraprofile axiom (among those we wanna use),
            # get the instances for this profile. Also pass the instances that reach the profile,
            # in case some heuristic is in place.
            for axiom in intraAxioms(axioms_to_use):
                I_prime = axiom.getInstances(profile, goal, reachedBy[profile])
                I.update(I_prime)

            # same for derived axioms.
            for derived_axiom in derived_axioms(axioms_to_use):
                I_prime = derived_axiom.getInstancesAndProfiles(profile, goal, reachedBy[profile])
                I.update(I_prime)

            # if the current depth < max depth, also expand the inter-profile instances.
            # (max_depth = None ---> no bound)
            if (MAX_DEPTH is None or depth < MAX_DEPTH):
                for axiom in interAxioms(axioms_to_use):
                    P_prime = axiom.getInstancesAndProfiles(profile, goal, reachedBy[profile])

                    # add reached profiles 
                    # to the queue, with a depth+1
                    for p, inst in P_prime:
                        fifo.append((p, depth+1))
                        I.add(inst)
                        reachedBy[p].add(inst)

            # profile explored: no need to remember how it was reached, now.
            del reachedBy[profile]

    return I, P