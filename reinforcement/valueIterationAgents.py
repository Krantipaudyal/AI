# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for i in range(self.iterations):
            curVal = self.values.copy() 
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state) == False:
                    maxVal = -9999
                    for action in self.mdp.getPossibleActions(state):
                        val = 0
                        for transition in self.mdp.getTransitionStatesAndProbs(state, action):
                            val += transition[1] * (
                            self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
                        if val > maxVal:
                            maxVal = val
                    curVal[state] = maxVal
                else:
                    for action in self.mdp.getPossibleActions(state):
                        val = 0
                        for transition in self.mdp.getTransitionStatesAndProbs(state, action):
                            val += transition[1] * (
                            self.mdp.getReward(s, action, transition[0]) + self.discount * self.values[transition[0]])
                        curVal[state] = val
            self.values = curVal



                


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qval = 0
        transtionList = self.mdp.getTransitionStatesAndProbs(state, action)
        for transition in transtionList:
            qval += transition[1] * (
                self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
        return qval
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        allPossibleActions = self.mdp.getPossibleActions(state)
        if self.mdp.isTerminal(state) == False:
            bestAction = allPossibleActions[0]
            bestVal = self.getQValue(state, bestAction)
            for action in allPossibleActions:
                if self.getQValue(state, action) > bestVal:
                    bestVal = self.getQValue(state, action)
                    bestAction = action
            return bestAction
        #return self.actions[state]

        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        iterations = self.iterations
        states = self.mdp.getStates()
        for iteration in range (iterations):
            index = iteration % len(states)
            if not self.mdp.isTerminal(states[index]):
                action = self.computeActionFromValues(states[index])
                self.values[states[index]] = self.computeQValueFromValues(states[index], action)



class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        ##dictionary 
        #predecessor = {}
        #pq = util.PriorityQueue()

        ##creates set for every state
        #for state in self.mdp.getStates():
        #    predecessor[state] = []

        #for state in self.mdp.getStates():
        #    if not self.mdp.isTerminal(state):
        #        listVal = []
        #        for possibleAction in self.mdp.getPossibleActions(state):
        #            listVal.append(self.computeQValueFromValues(state, possibleAction))
        #        difference = abs(self.values[state] - max(listVal))
        #        pq.push(state, -difference)

        #        #updates predecessor
        #        for possibleAction in self.mdp.getPossibleActions(state):
        #            for i in self.mdp.getTransitionStatesAndProbs(state, possibleAction):
        #                if predecessor[i[0]].count(state) == 0:
        #                    predecessor[i[0]].append(state)

        #for iteration in range(self.iterations):
        #    if pq.isEmpty():
        #        break
        #    state = pq.pop()
        #    listVal = []
        #    for currAction in self.mdp.getPossibleActions(state):
        #        listVal.append(self.computeQValueFromValues(state, currAction))
        #    self.values[state] = max(listVal)

        #    for p in predecessor[state]:
        #        listVal = []
        #        for currAction in self.mdp.getPossibleActions(p):
        #            listVal.append(self.computeQValueFromValues(p, currAction))
        #        difference = abs(self.values[p] - max(listVal))
        #        if difference > self.theta:
        #            pq.update(p, -diff)

        predecessors = {}
        pq = util.PriorityQueue()
        for state in self.mdp.getStates():
            predecessors[state] = []
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                #updating queue
                listVal = []
                for currAction in self.mdp.getPossibleActions(state):
                    listVal.append(self.computeQValueFromValues(state, currAction))
                diff = abs(self.values[state] - max(listVal))
                pq.push(state, -diff)
                #updating predecessors
                for a in self.mdp.getPossibleActions(state):
                    for k in self.mdp.getTransitionStatesAndProbs(state, a):
                        if predecessors[k[0]].count(state) == 0:
                            predecessors[k[0]].append(state)

        for i in range(self.iterations):
            if pq.isEmpty():
                break
            s = pq.pop()
            valuelist = []
            for currAction in self.mdp.getPossibleActions(s):
                valuelist.append(self.computeQValueFromValues(s, currAction))
            self.values[s] = max(valuelist)

            for p in predecessors[s]:
                valuelist = []
                for currAction in self.mdp.getPossibleActions(p):
                    valuelist.append(self.computeQValueFromValues(p, currAction))
                diff = abs(self.values[p] - max(valuelist))
                if diff > self.theta:
                    pq.update(p, -diff)

