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
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        distance_ghost = [(manhattanDistance(newPos,newghost.getPosition())+newghost.scaredTimer) for newghost in newGhostStates]
        if min(distance_ghost) <= 1:
            return 0


        distance_food = currentGameState.getFood().asList()
        closest_food = min([manhattanDistance(newPos,food) for food in distance_food])
        return  scoreEvaluationFunction(successorGameState) -closest_food 

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        def minmax(gameState,agent,depth):
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState), 0
            
            if agent == gameState.getNumAgents()-1:
                nextAgent = 0
                depth += 1 
            else:
                nextAgent = agent + 1

            result = []
            first = True
            for action in gameState.getLegalActions(agent):
                nextValue = minmax(gameState.generateSuccessor(agent,action),nextAgent,depth)
                if first: 
                    result.append(nextValue[0])
                    result.append(action)
                    first = False
                else:
                    if agent == self.index:
                        if nextValue[0] > result[0]:
                            result[0] = nextValue[0]
                            result[1] = action
                    else:
                        if nextValue[0] < result[0]:
                            result[0] = nextValue[0]
                            result[1] = action

            return result
        return minmax(gameState,0,0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def a_b(gameState,agent,depth,a,b):
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState), 0
            
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = self.index
            else:
                nextAgent = agent + 1
             
            result = []
            first = True
            for action in gameState.getLegalActions(agent):
                nextValue = a_b(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)
                if first: 
                    result.append(nextValue[0])
                    result.append(action)
                    first = False
                else:
                    if agent == 0:
                        if nextValue[0] > result[0]:
                            result[0] = nextValue[0]
                            result[1] = action
                    else:
                        if nextValue[0] < result[0]:
                            result[0] = nextValue[0]
                            result[1] = action

                if (result[0] > b and agent == self.index) or (result[0] < a and agent != self.index):
                    return result

                if agent == self.index:
                    if (a < result[0]):
                        a = result[0]
                else:
                    if (b > result[0]):
                        b = result[0]           
            return result
        int_max = 9999999999999999999999
        return a_b(gameState,self.index,0, -int_max, int_max)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectic_max(gameState,agent,depth):
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState), 0
            
            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = self.index
            else:
                nextAgent = agent + 1

            result = []
            first = True
            for action in gameState.getLegalActions(agent):
                nextValue = expectic_max(gameState.generateSuccessor(agent,action),nextAgent,depth)
                if first:
                    if(agent != self.index):
                        result.append((nextValue[0] / len(gameState.getLegalActions(agent))))
                        result.append(action)
                    else:
                        result.append(nextValue[0])
                        result.append(action)
                    first = False
                else:
                    if agent == self.index:
                        if nextValue[0] > result[0]:
                            result[0] = nextValue[0]
                            result[1] = action
                    else:
                        result[0] = result[0] + (nextValue[0] / len(gameState.getLegalActions(agent)))
                        result[1] = action
            return result

        return expectic_max(gameState,self.index,0)[1]


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return 1001

    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]


    score = currentGameState.getScore()

    nearestFood = min([util.manhattanDistance(currentPos, food) for food in currentFood])
    score += -len(currentGameState.getCapsules()) - len(currentFood) + float(1/nearestFood)
    
    nearestCurrentGhost = min([manhattanDistance(currentPos, ghost.getPosition()) for ghost in currentGhostStates])
    scaredTime = sum(currentScaredTimes)
    
    if nearestCurrentGhost >= 1:
        if scaredTime <= 1:
            score += -1/nearestCurrentGhost
        else:
            score += 1/nearestCurrentGhost
    return score

# Abbreviation
better = betterEvaluationFunction
