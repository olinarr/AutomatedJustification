import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict

brackets = re.compile('\[.*?\]')

def drawGraph(answer = None):

    instances = fromAnswer(answer)
    
    G = nx.MultiGraph()
    G.add_edges_from(instances.keys())
    pos = nx.spring_layout(G)
    plt.figure()    
    nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
    node_size=500,node_color='pink',alpha=0.9,\
    labels={node:node for node in G.nodes()})

    nx.draw_networkx_edge_labels(G, pos, edge_labels=instances, font_color='red')
    plt.axis('off')
    plt.show()

def fromAnswer(answer):

    name2lab = {"[CANCELLATION]" : "can", "[GOAL]" : "goal", "[CONDORCET]" : "con",
        "[POSITIVE RESPONSENESS]" : "pos", "[NEUTRALITY]" : "neu", "[REINFORCEMENT]" : "rei",
        "[FAITHFULNESS]" : 'fai', "[PARETO]" : 'par', "[AT LEAST ONE]" : 'at_least_one',
        "[POSITIVE RESPONSENESS, CANCELLATION]": "pos+can"}

    instances, all_p = defaultdict(list), set()

    for line in answer.split('\n'):
        bracketed = brackets.findall(line)

        if bracketed and "GOAL" in bracketed[0]:
            goal_profile = bracketed[1]

    for line in answer.split('\n'):
        bracketed = brackets.findall(line)

        if len(bracketed) <= 1:
            continue

        instance, profiles = bracketed[0], set(bracketed[1:])

        profiles = list(profiles)

        all_p = all_p.union(profiles)

        if len(profiles) == 1:
            instances[(profiles[0], profiles[0])].append(name2lab[instance])
        elif len(profiles) == 2:
            instances[(profiles[0], profiles[1])].append(name2lab[instance])
        elif len(profiles) == 3:
            main = bracketed[-1]
            p, q = bracketed[1], bracketed[2]
            instances[(main, p)].append(name2lab[instance])
            instances[(main, q)].append(name2lab[instance])
        else:
            raise NotImplementedError()

    def transform(x):
        goal = x == goal_profile

        x = x.replace('[', '')
        x = x.replace(']', '')
        x = x.replace(', ', '\n')
        x = x.split('\n')
        x = '\n'.join(map(lambda _: _[1:], x))
        
        if goal:
            x = '<GOAL>\n' + x

        return x

    new_instances = {}
    for k, insts in instances.items():
        new_instances[tuple(map(transform, k))] = '+'.join(insts)
        

    return new_instances