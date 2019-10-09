import math
import pickle
import time

class Node:
  def __init__(self, number, transport, cost, depth, goal, antecessor, auxheur, tickets):
    self.number = number
    self.transport = transport
    self.depth = depth

    selfXY = auxheur[number - 1]
    goalXY = auxheur[goal - 1]

    self.cost = cost
    self.heuristic = math.hypot(goalXY[0] - selfXY[0], goalXY[1] - selfXY[1]) + cost
    self.antecessor = antecessor
    self.sucessors = []
    self.tickets = tickets
  
  def __lt__(self, other):
    return self.heuristic < other.heuristic

class Tree:
  def __init__(self, expansions, depth, goal, auxheur):
    self.toExpand = []
    self.expansions = expansions
    self.maxDepth = depth
    self.goal = goal
    self.auxheur = auxheur

    self.possiblePaths = []

  def expandNext(self, model):
    if (self.expansions == 0):
      print("Expansion Limit Reached!")
      return -1

    node = self.toExpand.pop(0)
    nodeDepth = node.depth
    possibilities = model[node.number]

    for possibility in possibilities:
      if node.tickets[possibility[0]] > 0:
        newNode = Node(possibility[1],possibility[0], node.heuristic ,nodeDepth + 1, self.goal, node, self.auxheur, node.tickets.copy())
        self.toExpand.append(newNode)
        node.sucessors.append(newNode)

        newNode.tickets[possibility[0]] -= 1
        self.expansions -= 1

        if (possibility[1] == self.goal):
          self.possiblePaths.append(newNode)
    
    self.toExpand.sort()
    return self.possiblePaths

def testPath(result):
  depths = []

  for detective in result:
    tempSet = set()
    for possibility in detective:
      tempSet.add(possibility.depth)
    
    depths.append(tempSet)
  
  intersectionSet = depths[0]
  for x in range(len(depths) - 1):
    ##print(intersectionSet)
    intersectionSet = intersectionSet.intersection(depths[x + 1])

  nodes = []
  if len(intersectionSet) != 0:
    commonDepth = intersectionSet.pop()
    for detective in result:
      i = 0
      while detective[i].depth != commonDepth:
        i += 1
      
      nodes.append(detective[i])

  return nodes
  
def getPath(nodes):
    result = []

    while (nodes[0].antecessor != None):
      transports = []
      numbers = []
      newNodes = []

      for node in nodes:
        transports.append(node.transport)
        numbers.append(node.number)
        newNodes.append(node.antecessor)

      result = [[transports, numbers]] + result
      nodes = newNodes

    numbers = []
    for node in nodes:
      numbers.append(node.number)

    result = [[[], numbers]] + result
    return result

class SearchProblem:

  def __init__(self, goal, model, auxheur = []):

    self.goal = goal
    self.model = model
    self.auxheur = auxheur

    pass

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
    ## print("Modelo: " + str(self.model))
    ## print("Tamanho: " + str(len(self.model)))
    ## print("Auxheur: " + str(self.auxheur))
    ## print("Tamanho: " + str(len(self.auxheur)))

    forest = []

    for i in range(len(init)):
      expansionTree = Tree(limitexp, limitdepth, self.goal[i], self.auxheur)
      initialNode = Node(init[i], None, 0, 0, self.goal[i], None, self.auxheur, tickets)
      expansionTree.toExpand.append(initialNode)
      forest.append(expansionTree)

    gotIt = False
    while not gotIt:
      gotIt = True
      result = []

      for tree in forest:
        result.append(tree.expandNext(self.model))
        gotIt = gotIt and len(result[-1]) != 0

      if gotIt:
        nodes = testPath(result)
        gotIt = len(nodes) != 0
    
    result = getPath(nodes)
    return result
    