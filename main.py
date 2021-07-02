# Main interface

import argparse
from Helpers import powerset
from time import time
from Profile import Profile
from core import iterjustify
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--p', type=str, help='Goal profile. Example: 2:012,1:210 or 012,012,210 (Both mean {#2:0>1>2, #1:2>1>0})')
parser.add_argument('--o', type=str, help='Goal outcome. Default: try all! Example: 01 (means {0, 1})', default = None)
parser.add_argument('--max_depth', type=int, help='Depth of the search. Default: unbounded', default = None)
parser.add_argument('--corpus', type=str, default='corpus.txt', help='Axiom corpus.')
parser.add_argument('--time', action='store_true', help='Print time performance.')
parser.add_argument('--limit', type=int, help='Number of MUSes to search through (return only the smallest among these). Default: one.', default = 1)
parser.add_argument('--random', action='store_true', help='Generate random profile. Specify --gen for generation method, --n and --m!')
parser.add_argument('--gen', type=str, help='Strategy to randomly generate. Options: polya, walsh, conitzer', default = 'polya')
parser.add_argument('--alpha', type=float, help='Polya-Eggenberg Urn model: contagion parameter. Default: 0 (= Impartial Culture)', default = 0)
parser.add_argument('--n', type=int, help='When generating a random profile, specifies the number of voters.')
parser.add_argument('--m', type=int, help='When generating a random profile, specifies the number of alternatives.')
parser.add_argument('--preflib', action='store_true', help='Read from preflib profile. Specify --file, --n and --m!')
parser.add_argument('--file', type=str, help='File to read for preflib. No `.soc`, please!')
parser.add_argument('--draw', action='store_true', help='Draw answer.')
args = parser.parse_args()

PREFLIB_FOLDER = '/Preflib'

if args.random:

    assert args.o is None, "Can't specify outcome when dealing with random profiles."
    assert args.n is not None and args.m is not None, "Must specify --n and --m when generating a random profile!"
    assert not args.preflib, "Only one mode please! Either random or preflib"

    n, m = args.n, args.m

    print(f"Generating profile with {n} voters and {m} alternatives...", end=' ', flush = True)

    # Polya-Eggenberg Urn model for random profile
    if args.gen == 'polya':
        goal_profile = Profile.polyaUrn(n, m, args.alpha)
    # Toby Walsh's generation method for SinglePeaked profiles,
    # from "Generating Single Peaked Votes" (2015), https://arxiv.org/pdf/1503.02766.pdf
    elif args.gen == 'walsh':
        goal_profile = Profile.walshSinglePeaked(n, m)
    # Vincent Conitzer's generation method for SinglePeaked profiles,
    # from "Eliciting Single-Peaked Preferences Using Comparison Queries" (2009), https://www.jair.org/index.php/jair/article/view/10607
    elif args.gen == 'conitzer':
        goal_profile = Profile.conitzerSinglePeaked(n, m)
    else:
        raise Exception(f"Unknown random strategy; `{args.gen}`")
    goal_outcome = None # <-- we will try all
    print(f"Done.\nGenarated profile: {goal_profile.toString()}")


elif args.preflib:
    assert '.soc' not in args.file, 'Don`t specify the extension.'
    # function to parse preflib files
    from Preflib.readSoc import readPreflibString
    # parse it, and create a Profile
    goal_profile = Profile.fromString(readPreflibString(PREFLIB_FOLDER + args.file + '.soc', args.n, args.m))
    n = len(goal_profile)
    m = len(goal_profile.getAlternatives())
    goal_outcome = None # <-- we will try all

    print(f"Generated from Preflib the profile {goal_profile.toString()}.")

# manually specified profile
else:
    goal_profile = Profile.fromString(args.p)
    n = len(goal_profile)
    m = len(goal_profile.getAlternatives())
    # if none: we will try all
    goal_outcome = None if args.o is None else set(map(int, args.o))

# read axioms to use
with open(args.corpus, 'r') as f:
    axioms_to_use = f.read().split('\n')

if goal_outcome is not None:
    outcomesToCheck = {frozenset(goal_outcome)}
else:
    # we try all non empty outcomes. To get the alternatives, we look at the goal profile
    outcomesToCheck = set()
    for o in powerset(goal_profile.getAlternatives()):
        if o:
            outcomesToCheck.add(frozenset(o))

start = time()

# Try to find a justification! Returns the answers, depth of the found justification(s), generation and solving times
# answers contains: a nice text for the explanation, normative basis, the justified outcome, and size.
answers, depth, gen_time, sol_time = iterjustify(goal_profile, outcomesToCheck, axioms_to_use, args.max_depth, limit = args.limit)

elapsed = time() - start

# if we found one, print about it
if answers:
    print(f"Justified {len(answers)} outcome(s).")

    print()

    for answer, normative, outcome, size in answers:
        print(f"Justification for {set(outcome)}")
        print(f"Normative Basis: {set(normative)}")
        print()
        print(answer)
# tough luck!
else:
    print("No justification.")

if args.time:
    print(f'elapsed time: {elapsed:.2f}')

# draw explanation
if args.draw and answers:
    from drawGraph import drawGraph
    for answer, _, _, _ in answers:
        drawGraph(answer = answer)