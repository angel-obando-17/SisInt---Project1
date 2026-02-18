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

def depthFirstSearch( problem: SearchProblem ) -> List[ Directions ]:
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
    stack = util.Stack( )
    visited = set( )

    start = problem.getStartState( )

    stack.push( ( start, [ ] ) )

    goal = False
    directions = [ ]

    while not stack.isEmpty( ) and not goal:
        state, path = stack.pop( )
        if state not in visited:
            visited.add( state )
            if problem.isGoalState( state ):
                goal = True
                directions = path
            else:
                successors = problem.getSuccessors( state )
                for successor, action, stepCost in successors:
                    next_path = path + [ action ]    
                    stack.push( ( successor, next_path ) )

    return directions

def breadthFirstSearch( problem: SearchProblem ) -> List[ Directions ]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue( )
    visited = set( )

    start = problem.getStartState( )
    queue.push( ( start, [ ] ) )
    goal = False
    directions = [ ]

    while not queue.isEmpty( ) and not goal:
        state, path = queue.pop( )
        if state not in visited:
            visited.add( state )
            if problem.isGoalState( state ):
                goal = True
                directions = path
            else:
                succesors = problem.getSuccessors( state )
                for succesor, action, stepCost in succesors:
                    next_path = path + [ action ]
                    queue.push( ( succesor, next_path ) )
    
    return directions

def uniformCostSearch( problem: SearchProblem ) -> List[ Directions ]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontera = util.PriorityQueue()
    estadoInicial = problem.getStartState() 

    # Se inserta en la frontera: (estado, lista_de_acciones, costo_acumulado) con prioridad 0
    frontera.push( (estadoInicial, [], 0), 0 )
    visitados = set()
    while not frontera.isEmpty():

        # Se extrae el nodo con el menor costo acumulado
        estado, acciones, costoAcumulado = frontera.pop()

        if estado in visitados:
            continue

        visitados.add( estado )

        if problem.isGoalState( estado ):
            return acciones

        # Se expanden los sucesores del estado actual
        for sucesor, accion, costoPaso in problem.getSuccessors( estado ):

            if sucesor not in visitados:

                nuevoCosto = costoAcumulado + costoPaso  # Se calcula el nuevo costo acumulado sumando el costo del paso actual

                # Se inserta el sucesor en la frontera con su costo acumulado como prioridad
                frontera.push(
                    ( sucesor, acciones + [accion], nuevoCosto ),
                    nuevoCosto  # La prioridad es el costo total acumulado hasta este nodo
                )
    return []     # Si no se encontra la meta, se retorna lista vacía (sin solución)

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch( problem: SearchProblem, heuristic=nullHeuristic ) -> List[ Directions ]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # A* es como UCS pero la prioridad es f(n) = g(n) + h(n)
    # donde g(n) es el costo acumulado del camino recorrido
    # y h(n) es la estimación heurística al objetivo

    frontera = util.PriorityQueue()
    estadoInicial = problem.getStartState()

    # Calcular la heurística del estado inicial
    hInicial = heuristic( estadoInicial, problem )

    # Insertar en la frontera: (estado, acciones, costo_g) con prioridad f = g + h
    frontera.push( ( estadoInicial, [], 0 ), hInicial )

    # Diccionario que guarda el menor costo g con el que se expandió cada estado.
    # Esto permite re-expandir un estado si se descubre un camino más barato
    # (necesario cuando la heurística es inconsistente/no monótona).
    mejorCostoG = {}

    while not frontera.isEmpty():

        # Extraer el nodo con menor f(n) = g(n) + h(n)
        estado, acciones, costoG = frontera.pop()

        # Si este estado ya fue expandido con un costo g igual o menor, lo omitimos.
        # Si el nuevo costoG es menor, significa que hallamos un camino más barato
        # y debemos re-expandir el estado (condición para heurísticas inconsistentes).
        if estado in mejorCostoG and costoG >= mejorCostoG[ estado ]:
            continue

        # Registrar el mejor costo g conocido para este estado
        mejorCostoG[ estado ] = costoG

        if problem.isGoalState( estado ):
            return acciones

        # Expandir los sucesores del estado actual
        for sucesor, accion, costoPaso in problem.getSuccessors( estado ):

            nuevoCostoG = costoG + costoPaso #costo acumulado hasta el estado actual + costo del paso

            # Solo agregar a la frontera si encontramos un camino más barato al sucesor
            if sucesor not in mejorCostoG or nuevoCostoG < mejorCostoG[ sucesor ]:

                # h(sucesor) = estimación heurística desde el sucesor al objetivo
                hSucesor = heuristic( sucesor, problem )

                # f(sucesor) = g(sucesor) + h(sucesor)
                prioridad = nuevoCostoG + hSucesor

                frontera.push(
                    ( sucesor, acciones + [accion], nuevoCostoG ),
                    prioridad
                )

    return []  # Si no se encontró la meta, retornar lista vacía (sin solución)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
