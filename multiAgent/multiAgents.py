# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #do not stop
        badStop = 0
        if action == 'Stop':
            badStop = -100

        #results from food
        newFoodList = newFood.asList()
        min_food_distance = 1
        if newFoodList:
            min_food_distance = min(util.manhattanDistance(newPos, food) for food in newFoodList)

        #power Pallets
        palletList = successorGameState.getCapsules()
        min_pallet_distance = 1
        if palletList:
            min_pallet_distance = min(util.manhattanDistance(newPos, food) for food in palletList)

        #for ghost, stay away
        distance_to_ghost = 0
        for ghost in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost)
            if distance <= 1:
                distance_to_ghost += 1

        #scared ghost
        newScaredTimes = [ghostState.scaredTimer for ghostState in successorGameState.getGhostStates()]
        eatGhostReward = 0
        #getting the closest ghost
        closestGhost = min([manhattanDistance(newPos, x.getPosition()) for x in newGhostStates ])
        if min(newScaredTimes) > 0:
            eatGhostReward = 1/float(closestGhost)
        result = successorGameState.getScore()
        # 1/value because, we want to add big value so if the min number is very big, number being added will be very small
        # and if the min number is small, number being added will be big so we add big number like 1/1000 = 0.001 and 1/100 = 0.01 so we add 0.01
        result += 1/float(min_food_distance)  
        result += 1/float(min_pallet_distance)
        result += badStop
        result += -100 * distance_to_ghost
        result += eatGhostReward
        return result

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(agentIndex, depth, gameState):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1
            if agentIndex == 0:
                return max (minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                            for nextAction in actions)
            else:
                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                           for nextAction in actions)
        bestAction = Directions.WEST
        maximum = float("-inf")
        for action in gameState.getLegalActions(0):
            value = minimax(1, 0 , gameState.generateSuccessor(0, action))
            if value > maximum:
                maximum = value
                bestAction = action
        return bestAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        #DOES NOT WORK
        #

        #def minimax(agentIndex, depth,gameState, alpha, beta, maximizing):
        #    if depth == self.depth or gameState.isLose() or gameState.isWin() :
        #        return self.evaluationFunction(gameState)
        #    nextAgent = agentIndex + 1
        #    if maximizing:
        #        maxEval = float("-inf")
        #        for action in gameState.getLegalActions(agentIndex):
        #            if gameState.getNumAgents() == nextAgent:
        #                nextAgent = 0
        #                depth += 1
        #            eval = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)
        #                           ,alpha, beta, False)
        #            maxEval  = max(maxEval, eval)
        #            alpha =  max(alpha, eval)
        #            if beta <= alpha:
        #                break
        #            return maxEval
        #    else:                
        #        minEval = float("+inf")
        #        for action in gameState.getLegalActions(agentIndex):
        #            if gameState.getNumAgents() == nextAgent:
        #                nextAgent = 0
        #                depth += 1
        #            eval = minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)
        #                            ,alpha, beta, True)
        #            minEval  = min(minEval, eval)
        #            beta =  min(beta, eval)
        #            if beta <= alpha:
        #                break
        #            return minEval

        #            bestAction = Directions.WEST
        #maximum = float("-inf")
        #min = float("+inf")

        #for action in gameState.getLegalActions(0):
        #    value = minimax(1, 0 , gameState.generateSuccessor(0, action), maximum, min, True)
        #    if value > maximum:
        #        maximum = value
        #        bestAction = action
        #return bestAction

        #to calculate the evaluation of the first place
        value = (float("-inf"), "None")
        alpha = float("-inf")
        beta = float("+inf")
        legalActions = gameState.getLegalActions(0)
        for action in legalActions:
            value = max(value, (self.alphabeta(gameState.generateSuccessor(0, action),1, 0, alpha, beta), action))
            if value[0] > beta:
                return value[1]
            alpha = max(alpha, value[0])
        return value[1]

    #alphabeta pruning implementaion
    #taken help from https://www.youtube.com/watch?v=l-hh51ncgDI&t=585s&ab_channel=SebastianLague
    #modified minimax function to get here
    def alphabeta(self, gameState, agent, depth, alpha, beta):
        if agent >= gameState.getNumAgents():
            agent = 0
            depth += 1
       #checks if agent is at the end    
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legalActions = gameState.getLegalActions(agent)
        
        #maximizer basically
        if agent == 0:
            MaxValue = float("-inf")
            for action in legalActions:
                MaxValue = max(MaxValue, self.alphabeta(gameState.generateSuccessor(agent, action)
                                                        , agent + 1, depth, alpha, beta))
                #if breaks out of the loop if true
                # remaining gets pruned
                if MaxValue > beta:
                    return MaxValue
                alpha = max(alpha, MaxValue) #
            return MaxValue
        else:
            minValue = float("inf")
            for action in legalActions:
                minValue = min(minValue, self.alphabeta(gameState.generateSuccessor(agent, action)
                                                        , agent + 1, depth, alpha, beta))
                if minValue < alpha:
                    return minValue
                beta = min(beta, minValue)
            return minValue


        util.raiseNotDefined() 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        """
        "*** YOUR CODE HERE ***"
        def expectimax_search(state, agentIndex, depth):
            # if in min layer and last ghost
            if agentIndex == state.getNumAgents():
                # if reached max depth, evaluate state
                if depth == self.depth:
                    return self.evaluationFunction(state)
                # starts new layer with new depth
                else:
                    return expectimax_search(state, 0, depth + 1)
            # if not min layer and last ghost
            else:
                moves = state.getLegalActions(agentIndex)
                # if nothing can be done, evaluate the state
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                # get all the minimax values for the next layer with each node being a possible state after a move
                next = (expectimax_search(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

                # if max layer, return max of layer below
                if agentIndex == 0:
                    return max(next)
                # if min layer, return expectimax values
                else:
                    l = list(next)
                    return sum(l) / len(l)
        # select the action with the greatest minimax value
        result = max(gameState.getLegalActions(0), key=lambda x: 
                     expectimax_search(gameState.generateSuccessor(0, x), 1, 1))

        return result
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    same as evaluation functionn that was written for general ghost which counts
    rewards the pacman agent for eating ghost when scared, eating power pallet
    makes agent stay away from the ghosts, get to the closest food and to make the
    agent not thrash, manhattan distance formula has been used which calculates
    the shortest distance to the target
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    #results from food
    newFoodList = newFood.asList()
    min_food_distance = 1
    if newFoodList:
        min_food_distance = min(util.manhattanDistance(newPos, food) for food in newFoodList)

    #power Pallets
    palletList = currentGameState.getCapsules()
    min_pallet_distance = 1
    if palletList:
        min_pallet_distance = min(util.manhattanDistance(newPos, food) for food in palletList)

    #for ghost, stay away
    distance_to_ghost = 0
    for ghost in currentGameState.getGhostPositions():
        distance = util.manhattanDistance(newPos, ghost)
        if distance <= 1:
            distance_to_ghost += 1

    #scared ghost
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    eatGhostReward = 0
    #getting the closest ghost
    closestGhost = min([manhattanDistance(newPos, x.getPosition()) for x in newGhostStates ])
    if min(newScaredTimes) > 0:
        eatGhostReward = 1/float(closestGhost)
    result = currentGameState.getScore()
    # 1/value because, we want to add big value so if the min number is very big, number being added will be very small
    # and if the min number is small, number being added will be big so we add big number like 1/1000 = 0.001 and 1/100 = 0.01 so we add 0.01
    result += 1/float(min_food_distance)  
    result += 1/float(min_pallet_distance)
    result += -100 * distance_to_ghost
    result += eatGhostReward
    return result
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
