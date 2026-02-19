# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = set()
    parent = dict()

    start = problem.getStartState()
    stack.push(start)

    term = None
    goal = False

    while not stack.isEmpty() and not goal:
        u = stack.pop()

        if u in visited:
            continue

        visited.add(u)
        if problem.isGoalState(u):
            term = u
            goal = True
        else:
            successors = problem.getSuccessors(u)
            for v, act, _ in successors:
                if v not in visited:
                    parent[v] = (u, act)
                    stack.push(v)

    path = []
    if goal:
        u = term
        while u != start:
            u, act = parent[u]
            path.append(act)
        path.reverse()

    return path
  

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = set()
    parent = dict()

    start = problem.getStartState()
    queue.push(start)
    visited.add(start)

    term = None
    goal = False

    while not queue.isEmpty() and not goal:
        u = queue.pop()

        if problem.isGoalState(u):
            term = u
            goal = True
        else:
            successors = problem.getSuccessors(u)
            for v, act, _ in successors:
                if v not in visited:
                    visited.add(v)
                    parent[v] = (u, act)
                    queue.push(v)

    path = []
    if goal:
        u = term
        while u != start:
            u, act = parent[u]
            path.append(act)
        path.reverse()

    return path
    

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pqueue = util.PriorityQueue()
    parent = dict()
    dist = dict()

    start = problem.getStartState()

    dist[start] = 0
    pqueue.push((dist[start], start), dist[start])

    term = None
    goal = False

    while not pqueue.isEmpty() and not goal:
        du, u = pqueue.pop()

        if problem.isGoalState(u):
            term = u
            goal = True
        elif du == dist[u]:
            successors = problem.getSuccessors(u)
            for v, act, duv in successors:
                if not v in dist or du + duv < dist[v]:
                    dist[v] = du + duv
                    parent[v] = (u, act)
                    pqueue.push((dist[v], v), dist[v])

    path = []
    if goal:
        u = term
        while u != start:
            u, act = parent[u]
            path.append(act)
        path.reverse()

    return path

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pqueue = util.PriorityQueue()
    parent = dict()
    dist = dict()

    start = problem.getStartState()
    dist[start] = 0

    f = dist[start] + heuristic(start, problem)

    pqueue.push((dist[start], start), f)

    term = None
    goal = False

    while not pqueue.isEmpty() and not goal:
        du, u = pqueue.pop()
        if problem.isGoalState(u):
            term = u
            goal = True
        elif du == dist[u]:
            successors = problem.getSuccessors(u)
            for v, act, duv in successors:
                if not v in dist or du + duv < dist[v]:
                    dist[v] = du + duv
                    parent[v] = (u, act)
                    f = dist[v] + heuristic(v, problem)
                    pqueue.push((dist[v], v), f)
    path = []
    if goal:
        u = term
        while u != start:
            u, act = parent[u]
            path.append(act)
        path.reverse()

    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
