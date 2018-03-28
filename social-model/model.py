import logging
import sys
from random import random, uniform


class GlobalState:
    """Global state definition, as a model of population."""
    logger = logging.getLogger('GlobalState')
    _nodes = []
    _edges = []

    def getNodes(self):
        return self._nodes

    def neighbors(self, node):
        res = []
        for e in self._edges:
            if not node in e:
                continue
            node = list(e - {node})[0]
            res.append(node)
        return res

    def addEdge(self, node1, node2):
        if node1 == node2:
            self.logger.debug('same node, at both ends ' + str(node1.id))
            return
        edge = {node1, node2}
        nodes = list(edge)
        if (edge in self._edges):
            self.logger.debug('edge already present (%d<->%d)', nodes[0].id, nodes[1].id)
            return
        self._edges.append(edge)

    def removeEdge(self, node1, node2):
        edge = {node1, node2}
        nodes = list(edge)
        if (edge in self._edges):
            self.logger.debug('removing edge (%d<->%d)', nodes[0].id, nodes[1].id)
            self._edges.remove(edge)
        else:
            self.logger.debug('there was no that edge (%d<->%d)', nodes[0].id, nodes[1].id)

    def getEdges(self):
        return self._edges


class Citizen:
    """Each node representation. Citizen has:
opinion - like party choice
action - which determines if change of option is more comfortable
neighbors - as a edges in graph connected to this node
    """
    def __init__(self, id, opinion, action, pos=(0, 0)):
        self.id = id
        self.opinion = opinion
        self.action = action
        self.pos = pos
        self._neighbors = []

    def __str__(self):
        return (str(self.id), str(self.opinion), str(self.action))


def socialRemake(globalState, node, referenceLevel):
    logger = logging.getLogger('dif_ind_neigh')
    neig = globalState.neighbors(node)
    notNeigh = [n for n in globalState.getNodes() if n not in neig]

    rand = uniform(0, 1)
    if rand < referenceLevel:
        lmnotneigh = [m for m in notNeigh if node.opinion - m.action <= 0.5 and node.opinion - m.action >= -0.5]
        for d in lmnotneigh:
            logger.debug("adding edge for social remake")
            globalState.addEdge(node, d)
            break
    if rand > referenceLevel:
        diffneig = [l for l in neig if node.opinion - l.opinion > 0.5 or node.opinion - l.opinion < -0.5]
        for f in diffneig:
            logger.debug("removing edge for social remake")
            globalState.removeEdge(node, f)
            break


def differeciateIndividualNeighbor(globalState, node, referenceLevel):
    logger = logging.getLogger('dif_ind_neigh')
    rand = uniform(0, 1)
    if rand > referenceLevel:
        logger.debug("skiping")
        return
    # list of neighbors
    neighbors = globalState.neighbors(node)
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
        logger.debug("action changed - from %d to %d ", prev, node.action)
    elif diff >= 1:
        prev = node.action
        node.action = max(1, node.action - 1)
        logger.debug("action changed - from %d to %d ", prev, node.action)


def prepare_random_citizen(idx):
    randOpinion = uniform(0.5, 3.5)
    randAction = int(random() * 100) % 3 + 1
    return Citizen(idx, randOpinion, randAction, (random(), random()))


def main():
    FORMAT = '%(asctime)-15s %(levelname)-8s %(funcName)s:%(lineno)d - %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger('main')
    logger.info('so - starting')

    globalState = GlobalState()
    nodes = globalState.getNodes()
    logger.info('generating nodes')
    for idx in range(10):
        nodes.append(prepare_random_citizen(idx))
    logger.info('generating edges')
    for node in globalState.getNodes():
        for idx in range(1,4):
            otherEnd = nodes[(node.id + idx) % 10]
            globalState.addEdge(node, otherEnd)
    logger.info("stating with: nodes - %d, edges - %d", len(globalState.getNodes()), len(globalState.getEdges()))

    logger.info('processing')
    for timestep in range(100):
        logger.info('iteration - %d', timestep)
        troubled = [t for t in globalState.getNodes() if t.opinion - t.action >= 0.5 or t.opinion - t.action <= -0.5]
        logger.info("nodes - %d, edges - %d, troubled - %d",
                    len(globalState.getNodes()), len(globalState.getEdges()), len(troubled))
        for node in troubled:
            socialRemake(globalState, node, 0.7)
            differeciateIndividualNeighbor(globalState, node, 0.5)


if __name__ == "__main__":
    main()