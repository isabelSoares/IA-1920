# Isabel Soares (189466) & Rodrigo Sousa (189535) - Grupo 27
import random

# LearningAgent to implement
# no knowledeg about the environment can be used
# the code should work even with another environment
class LearningAgent:

        # init
        # nS maximum number of states
        # nA maximum number of action per state
        def __init__(self,nS,nA):

                self.nS = nS
                self.nA = nA
                
                self.alpha = 0.5
                self.gamma = 0.9275

                self.exploitation = 0.80
                self.explore = 1 - self.exploitation

                self.Q = [ [ 0 for i in range(nA) ] for j in range(nS) ]

        def selectBestIndex(self, st, aa):
                maxValue = self.Q[st][0]
                maxIndexes = [0]
                for i in range(len(aa)):
                        if (self.Q[st][i] > maxValue):
                                maxIndexes = []
                                maxIndexes.append(i)
                                maxValue = self.Q[st][i]
                        elif (self.Q[st][i] == maxValue):
                                maxIndexes.append(i)
                
                return maxIndexes[random.randint(0, len(maxIndexes) - 1)]


        # Select one action, used when learning  
        # st - is the current state        
        # aa - is the set of possible actions
        # for a given state they are always given in the same order
        # returns
        # a - the index to the action in aa
        def selectactiontolearn(self,st,aa):
                for i in range(len(aa), self.nA):
                        self.Q[st][i] = None

                randomValue = random.random()
                if (randomValue <= self.explore):
                        return random.randint(0, len(aa) - 1)
                else:
                        return self.selectBestIndex(st, aa)

        # Select one action, used when evaluating
        # st - is the current state        
        # aa - is the set of possible actions
        # for a given state they are always given in the same order
        # returns
        # a - the index to the action in aa
        def selectactiontoexecute(self,st,aa):                
                return self.selectBestIndex(st, aa)


        # this function is called after every action
        # st - original state
        # nst - next state
        # a - the index to the action taken
        # r - reward obtained
        def learn(self,st,nst,a,r):
                maxIndex = 0
                maxNext = self.Q[nst][0]
                for i in range(len(self.Q[nst])):
                        if self.Q[nst][i] != None and self.Q[nst][i] > maxNext:
                                maxNext = self.Q[nst][i]
                                maxIndex = i
        
                self.Q[st][a] = self.Q[st][a] + self.alpha * (r +  self.gamma * maxNext - self.Q[st][a])
                
                return
