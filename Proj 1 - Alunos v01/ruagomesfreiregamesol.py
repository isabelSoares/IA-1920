import math
import pickle
import time
import itertools

class Tree:
  
  def __init__(self, model, init):
    self.states = []
    self.toExpand = [init]
    self.model = model

  def addState(self, newState):
    self.states.append(newState)

  def expandState(self):
    stateToExpand = self.toExpand.pop(0)
    possibilities = []

    for pos in stateToExpand.pos:
      possibilities.append(self.model[pos])
    
    res = list(itertools.product(*possibilities))
    print(str(res))
    for possibilitie in res:
      positions = []
      tickets = stateToExpand.ticketsNeeded.copy()
      newPath = stateToExpand.path.copy()

      for detective in possibilitie:
        ##print(str(detective))
        positions.append(detective[1])
        tickets[detective[0]] += 1

      ##newPath[0] = newPath[0]
      newState = State(positions, stateToExpand.depth, stateToExpand, tickets, [])
      self.toExpand.append(newState)
      self.states.append(newState)

class State:

  def __init__(self, pos, depth, prev_state, tickets, path):
    self.pos = pos
    self.depth = depth
    self.antecessor = prev_state
    self.ticketsNeeded = tickets
    self.path = path

class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.model = model
    self.auxheur = auxheur

    initTickets = [0, 0, 0]

    self.goalState = State(goal, 0, None, initTickets, [[goal]])
    self.tree = Tree(model, self.goalState)
    for i in range(1000):
      self.tree.expandState()

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
    actualState = None
    for state in self.tree.states:
      if state.pos == init:
        actualState = state
        break

    print("Pos: " + str(actualState.pos))
    print("Tickets: " + str(actualState.ticketsNeeded))

    return actualState.path