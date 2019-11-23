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
                
                self.alpha = 0.2
                self.gamma = 0.9275

                self.tradeTrue = 0.95
                self.tradeFalse = 0.05

                self.Q = [ [ 0 for i in range(nA) ] for j in range(nS) ]

                #print(str(self.Q))
              
        
        # Select one action, used when learning  
        # st - is the current state        
        # aa - is the set of possible actions
        # for a given state they are always given in the same order
        # returns
        # a - the index to the action in aa
        def selectactiontolearn(self,st,aa):
                # print("select one action to learn better")

                a = 0
                maxValue = self.Q[st][0]
                for i in range(len(aa)):
                        if (self.Q[st][i] > maxValue and random.random() < self.tradeTrue) or (self.Q[st][i] <= maxValue and random.random() < self.tradeFalse):
                                maxValue = self.Q[st][i]
                                a = i

                for i in range(len(aa), self.nA):
                        self.Q[st][i] = None
                
                #print("Next Index: " + str(a))
                return a

        # Select one action, used when evaluating
        # st - is the current state        
        # aa - is the set of possible actions
        # for a given state they are always given in the same order
        # returns
        # a - the index to the action in aa
        def selectactiontoexecute(self,st,aa):
                # print("select one action to see if I learned")
                
                a = 0
                maxValue = self.Q[st][0]
                for i in range(len(aa)):
                        if self.Q[st][i] != None and self.Q[st][i] > maxValue:
                                maxValue = self.Q[st][i]
                                a = i
                
                #print("Next Index: " + str(a))
                return a


        # this function is called after every action
        # st - original state
        # nst - next state
        # a - the index to the action taken
        # r - reward obtained
        def learn(self,st,nst,a,r):
                #print("learn something from this data")

                maxIndex = 0
                maxNext = self.Q[nst][0]
                for i in range(len(self.Q[nst])):
                        if self.Q[nst][i] != None and self.Q[nst][i] > maxNext:
                                maxNext = self.Q[nst][i]
                                maxIndex = i

                #print("Old Value: " + str(self.Q[st][a]))
                #print("Parameters: r:" + str(r))
                self.Q[st][a] = self.Q[st][a] + self.alpha * (r +  self.gamma * maxNext - self.Q[st][a])
                #print("New Value: " + str(self.Q[st][a]))
                
                return
