# This file handles most of the SAT related stuff.


from Profile import Profile
import subprocess

class SATEncoding():

    def __init__(self, profiles, A):
        self.mapping = {}
        self.A = A

        # mapping from (profile, alternative) ---> propositional variable (non-zero integer index.)
        for profile in profiles:
            for x in self.A:
                self.mapping[(profile, x)] = len(self.mapping) + 1

    def getLiteral(self, profile, x):
        # get propositional var
        return self.mapping[(profile, x)]

    # Auxiliary function called from getJustification
    # (might want to check that one first):
    # from the SAT encoding of the instances 
    # creates a file that the gMUS extractor
    # can understand.
    def _dumpGroupCNF(self, instance2clauses):

        # first, we associates to each instance, an index.

        index2inst = list(instance2clauses.keys())
        # index + 1 because somehow ID=0 is not handled by MARCO (gMUS extractor), 
        # so we need to start from 1. Will need to pay attention to this while extacting
        # the output
        inst2index = {index2inst[index]:index+1 for index in range(len(index2inst))}

        with open('dump.gcnf', 'w') as file:

            # number of propositional vars, group of clauses (=instance) and of clauses in total
            nbVariables = len(self.mapping)
            nbGroups = len(instance2clauses)
            nbClauses   = 0
            for clauses in instance2clauses.values():
                nbClauses += len(clauses)


            # file header
            file.write("p gcnf " + str(nbVariables) + " " + str(nbClauses) + " " + str(nbGroups) + "\n")


            goal_index = None
            for instance, clauses in instance2clauses.items():
                # extract the goal index, we will need to return this
                if instance.axiomName() == 'Goal':
                    goal_index = inst2index[instance]
                
                # encode each instance (group of clauses)
                for clause in clauses:
                    line = "{" + str(inst2index[instance]) + "} "
                    for literal in clause:
                        line += str(literal) + " "
                    line += "0 \n"
                    file.write(line)

        # write file... and return the mapping from index to instance and the goal index
        # (we will need these to read the output of the gMUS extractor)

        return index2inst, goal_index

    # function to extract the justifications
    # accept a mapping from instance to sat encoding and limit (<- number of gMUSes to extract)
    def getJustification(self, instance2clauses, limit = 1):
        # this function create a file called dump.gcnf, containing all the info for the gMUS extraction
        # furthermore, returns data useful to read the output of the gMUS extractor
        index2inst, goal_index = self._dumpGroupCNF(instance2clauses)

        # call the gMUS searcher (marco)

        if limit != -1:
            command = ["gMUS/marco.py", "-v", "--parallel", "MUS,MUS,MUS,MUS,MUS,MUS,MUS,MUS", "-l", str(limit), "dump.gcnf"]
        else:
            command = ["gMUS/marco.py", "-v", "--parallel", "MUS,MUS,MUS,MUS,MUS,MUS,MUS,MUS", "dump.gcnf"]

        process = subprocess.run(command, stdout=subprocess.PIPE)

        outputSolver = process.stdout.decode('utf-8')
        lines = [line for line in outputSolver.split("\n") if len(line) != 0 and line[0] == 'U'] # Only get MUSes

        # ready to read
        justifications = []

        # each line is a gMUS
        for line in lines: 
            # get indexes of clauses in gMUS
            listIDs = [tmp for tmp in line.split(" ")]
            listIDs = listIDs[1:] # Remove 'U' to only keep IDs
            # -1 because I had to add 1 to the indexes, see above when generating the mapping! in self._dumpGroupCNF()
            listIDs = [int(id)-1 for id in listIDs]

            # if goal_index not in the gMUS, then we do not care about this gMUS
            # (again, -1 because of indexing problems, see above)
            if goal_index-1 in listIDs:
                # turn the indexes to the corresponding instances by the index2inst structure
                # given an Instance object, getExplanation() returns some text to be used in the explanation
                explanation = [index2inst[ID].getExplanation() for ID in listIDs]

                # normative basis: simply set of axioms we use
                normative = set()
                for ID in listIDs:
                	normative.update(index2inst[ID].normativeBasis())
                # ok, done!
                justifications.append((normative, explanation))


        # if we found at least one gMUS with the GOAL inside:
        if justifications:

            # Find Shortest gMUS (Return only that one)
            min_len = tuple()
            for normative, explanation in justifications:
                if min_len == tuple() or min_len[-1] > len(explanation):
                    min_len = (normative, explanation, len(explanation))

            return min_len[0], min_len[1]
        # else, sorry.
        else:
            return None, None

