import math
import pickle
import time

class Detective:

  def __init__(self, init):
    self.states = [init]
    self.toExpand = [init]
    self.stateGoal = None
    self.expansions = 0
    self.solved = False

  def expandState(self, nodesBFS, model, maxDepth, maxExpansion, anyorder):
    stateToExpand = self.toExpand.pop(0)
    if stateToExpand.depth >= maxDepth or self.expansions >= maxExpansion:
      return

    self.expansions += 1
    tmp = [[]]
    for x in range(0, len(stateToExpand.nodes)):
      subtmp = []
      possibilities = model[stateToExpand.nodes[x].pos]
      # print("Possibilities: " + str(possibilities))
      for tmpValue in tmp:
        for possibility in possibilities:
          # print("tmpValue: " + str(tmpValue))
          # print("possibilty: " + str(possibility))
          newValue = tmpValue + ([possibility])
          # print("newValue: " + str(newValue))
          subtmp.append(newValue)
      
      tmp = subtmp.copy()

    # print(str(tmp))

    possibilitiesStates = tmp
    for possibility in possibilitiesStates:
      tmpNodes = []
      tmpTickets = stateToExpand.ticketsLeft.copy()
      tmpPath = stateToExpand.pathTo.copy()
      tmpPath.append([[], []])

      # Number of detectives
      for part in possibility:
        tmpNode = nodesBFS[part[1]]
        if tmpNode not in tmpNodes:
          tmpNodes.append(tmpNode)
          tmpPath[-1][0].append(part[0])
          tmpPath[-1][1].append(part[1])
          tmpTickets[part[0]] -= 1
      
      if len(tmpNodes) == len(stateToExpand.nodes):
        validTickets = True
        for ticket in tmpTickets:
          if ticket < 0:
            validTickets = False
        
        # print(str(tmpPath))
        if validTickets:
          tmpState = State(tmpNodes, stateToExpand.depth + 1, stateToExpand.soFarCost + 1, tmpTickets, anyorder)
          tmpState.pathTo = tmpPath.copy()
          self.states = [tmpState] + self.states
          self.toExpand = [tmpState] + self.toExpand

    self.toExpand.sort()
    # print(self.toExpand)

  def checkSolved(self, goals, anyorder):
    stop = True

    if len(self.toExpand) == 0:
      return True

    possibleSolution = self.toExpand[0]
    possibleSolutionsPos = []
    for x in range(0, len(goals)):
      # print("Goal x: " + str(goals[x]))
      # print("Actual x: " + str(possibleSolution.nodes[x].pos))
      # print("Actual Cost: " + str(possibleSolution.orderFactor))
      possibleSolutionsPos.append(possibleSolution.nodes[x].pos)
      if (not anyorder) and (goals[x] != possibleSolution.nodes[x].pos):
        return False

    if anyorder:
      goals.sort()
      possibleSolutionsPos.sort()
      # print("Goal x: " + str(goals))
      # print("Actual x: " + str(possibleSolutionsPos))
      if goals != possibleSolutionsPos:
        return False

    self.solved = True
    return True

class State:

  def __init__(self, nodes, depth, cost, tickets, anyorder):
    self.nodes = nodes
    numberDetectives = len(nodes)

    self.depth = depth
    self.soFarCost = cost
    self.ticketsLeft = tickets

    self.heuristic = 0
    if not anyorder:
      for x in range(0, numberDetectives):
        if self.nodes[x].heur[x] > self.heuristic:
          self.heuristic = self.nodes[x].heur[x]
    
    else:
      tmp = [[]]
      for x in range(0, numberDetectives):
        subtmp = []
        possibilities = self.nodes[x].heur
        # print("Possibilities: " + str(possibilities))
        for tmpValue in tmp:
          for possibility in possibilities:
            # print("tmpValue: " + str(tmpValue))
            # print("possibilty: " + str(possibility))
            newValue = tmpValue + ([possibility])
            # print("newValue: " + str(newValue))
            subtmp.append(newValue)
        tmp = subtmp.copy()
      
      self.heuristic = math.inf
      for possibility in tmp:
        max = 0
        for x in range(0, numberDetectives):
          if possibility[x] > max:
            max = possibility[x]
        
        if max < self.heuristic:
          self.heuristic = max


    self.orderFactor = self.soFarCost + self.heuristic
    self.pathTo = []
  
  def __repr__(self):
    return str(self.nodes) + " " + str(self.depth)
  def __str__(self):
    return str(self.nodes) + " " + str(self.depth)
  def __lt__(self, other):
    return self.orderFactor < other.orderFactor

class Tree:
  # Class used to build a BFS tree i order to give correct heurisitcs to the various nodes!
  def __init__(self):
    self.nodes = {}
    self.toExpand = []
    pass

  # Expands the last node on Array toExpand
  def expandNode(self, model, goalIndex):
    nodeToExpand = self.toExpand.pop(0)
    possiblities = model[nodeToExpand.pos]

    for possiblity in possiblities:
      if possiblity[1] not in self.nodes:
        newHeur = nodeToExpand.heur.copy()
        newNode = Node(possiblity[1], newHeur)
        self.nodes[possiblity[1]] = newNode

        newNode.heur[goalIndex] += 1
        self.toExpand.append(newNode)
      
      else:
        newNode = self.nodes.get(possiblity[1])
      
        if (newNode.counterTemp != goalIndex):
          newNode.heur[goalIndex] = nodeToExpand.heur[goalIndex] + 1
          newNode.counterTemp += 1
          self.toExpand.append(newNode)

  # Expands Tree till every node has an heuristic
  def expandTillEnd(self, model, goalIndex):
    while (len(self.toExpand) != 0):
      self.expandNode(model, goalIndex)


class Node:

  def __init__(self, pos, heur):
    self.pos = pos
    self.heur = heur
    self.counterTemp = 0
  
  def __repr__(self):
    return str(self.pos)
  def __str__(self):
    return str(self.pos)

class SearchProblem:

  def __init__(self, goal, model, auxheur = []):

    self.goals = goal
    self.model = model
    self.auxheur = auxheur

    self.treeBFS = Tree()

    heur = []
    for x in range(0, len(self.goals)):
      heur.append(0)

    counter = 0
    for goal in self.goals:
      if (goal not in self.treeBFS.nodes):
        newNode = Node(goal, heur.copy())
        self.treeBFS.nodes[goal] = newNode
      else:
        newNode = self.treeBFS.nodes.get(goal)
        newNode.counterTemp = counter

      self.treeBFS.toExpand.append(newNode)
      self.treeBFS.expandTillEnd(self.model, counter)
      # print(str(self.treeBFS.nodes))

      counter += 1

    self.detective = None
    
    pass

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    
    nodesInit = []
    for initPos in init:
      initNode = self.treeBFS.nodes[initPos]
      nodesInit.append(initNode)

    initState = State(nodesInit, 0, 0, tickets, anyorder)
    initState.pathTo = [[[None], init]]
    # print(initState)

    self.detective = Detective(initState)
    while not self.detective.checkSolved(self.goals, anyorder):
      self.detective.expandState(self.treeBFS.nodes, self.model, limitdepth, limitexp, anyorder)
    
    if not self.detective.solved:
      print("No valid path found!")
      return None

    solution = self.detective.toExpand[0]
    # print("Expansions: " + str(self.detective.expansions))
    # print(str(solution.pathTo))
    return solution.pathTo
    