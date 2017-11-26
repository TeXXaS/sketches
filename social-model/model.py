import logging
import sys
from random import random, uniform


class GlobalState:
    _nodes = []

    def nodes(self):
        return self._nodes

    def neighbors(self, node):
        return []


class Citizen:
    def __init__(self, opinion, action, pos=(0, 0)):
        self.opinion = opinion
        self.action = action
        self.pos = pos

    def __str__(self):
        return (str(self.opinion), str(self.action))

    def neighbors(self, globalState):
        return globalState.neighbors(self)


def socialremake(globalState, node, b):
    neig = globalState.neighbors(node)
    notneigh = [n for n in globalState.nodes() if n not in neig]

    rand = uniform(1, 6)
    if rand < b:
        lmnotneigh = [m for m in notneigh if node.opinion - m.action <= 0.5 and node.opinion - m.action >= -0.5]
        for d in lmnotneigh:
            globalState.add_edge(node, d)
            print("edge added")
            break
    if rand > b:
        diffneig = [l for l in neig if node.opinion - l.opinion > 0.5 or node.opinion - l.opinion < -0.5]
        for f in diffneig:
            globalState.remove_edge(node, f)
            print("edge removed")
            break


def dif_ind_neigh(globalState, node, referenceLevel):
    logger = logging.getLogger('dif_ind_neigh')
    rand = uniform(0, 1)
    logger.debug(" dice " + str(rand))
    if rand > referenceLevel:
        logger.debug("skiping")
        return
    # list of neighbors
    neighbors = node.neighbors(globalState)
    # checking agains div by zero
    if len(neighbors) == 0:
        logger.debug("no neighbors - skipping")
        return
    # and all their actions
    actionNeighbors = []
    for neighbor in neighbors:
        actionNeighbors.append(neighbor.action)
    # avg action value
    averageActionNeighbors = sum(actionNeighbors) / len(neighbors)
    diff = node.action - averageActionNeighbors
    if diff <= -1:
        prev = node.action
        node.action += 1
        logger.debug("action changed - from " + str(prev) + " to " + str(node.action))
    elif diff >= 1:
        prev = node.action
        node.action = max(1, node.action - 1)
        logger.debug("action changed - from " + str(prev) + " to " + str(node.action))


def prepare_random_citizen():
    randOpinion = uniform(0.5, 3.5)
    randAction = int(random() * 100) % 3 + 1
    return Citizen(randOpinion, randAction, (random(), random()))


def main():
    FORMAT = '%(asctime)-15s %(levelname)-8s %(funcName)s:%(lineno)d - %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger('main')
    logger.info('so - starting')

    globalState = GlobalState()
    logger.info('generating')
    for idx in range(100):
        globalState.nodes().append(prepare_random_citizen())

    logger.info('processing')
    for timestep in range(100):
        troubled = [t for t in globalState.nodes() if t.opinion - t.action >= 0.5 or t.opinion - t.action <= -0.5]
        for node in troubled:
            socialremake(globalState, node, 0.7)
            dif_ind_neigh(globalState, node, 0.5)


main()
