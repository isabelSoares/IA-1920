import math
import pickle
import time

class Node:
  def __init__(self, number, transport, depth, goal, antecessor, auxheur):
    self.number = number
    self.transport = transport
    self.depth = depth

    selfXY = auxheur[number - 1]
    goalXY = auxheur[goal - 1]

    self.heuristic = math.hypot(goalXY[0] - selfXY[0], goalXY[1] - selfXY[1])
    self.antecessor = antecessor
    self.sucessors = []
  
  def __lt__(self, other):
    return self.heuristic < other.heuristic

class Tree:
  def __init__(self, expansions, depth, goal, auxheur):
    self.toExpand = []
    self.expansions = expansions
    self.maxDepth = depth
    self.goal = goal
    self.auxheur = auxheur

  def expandNext(self, model):
    if (self.expansions == 0):
      print("Expasion Limit Reached!")
      return -1

    foundGoal = False
    node = self.toExpand.pop(0)
    nodeDepth = node.depth
    possibilities = model[node.number]

    for possibility in possibilities:
      newNode = Node(possibility[1], possibility[0], nodeDepth + 1, self.goal, node, self.auxheur)
      self.toExpand.append(newNode)
      self.expansions -= 1

      if (possibility[1] == self.goal):
        foundGoal = True
    
    self.toExpand.sort()
    return foundGoal

  def getPath(self):
    result = []
    node = self.toExpand[0]

    while (node.antecessor != None):
      print(node.antecessor.number)
      result = [[[node.transport], [node.number]]] + result
      node = node.antecessor

    result = [[[], [node.number]]] + result
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

    expansionTree = Tree(limitexp, limitdepth, self.goal[0], self.auxheur)
    initialNode = Node(init[0], None, 0, self.goal[0], None, self.auxheur)
    expansionTree.toExpand.append(initialNode)

    gotIt = False
    while not gotIt:
      gotIt = expansionTree.expandNext(self.model)
    
    return expansionTree.getPath()
    