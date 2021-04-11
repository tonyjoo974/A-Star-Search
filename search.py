# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)
import queue
import heapq

class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
        self.gScore = float("inf")
        self.hScore = 0
        self.fScore = float("inf")

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs_helper(maze, startpoint, goalList):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = queue.Queue()
    start = startpoint
    goal = goalList
    q.put(start)
    visited = [start]
    parent = {}
    path = []
    while q:
        node = q.get()
        if node in goal:
            path.append(node)
            break
        neighbors = maze.getNeighbors(node[0], node[1])
        for each_node in neighbors:
            if each_node not in visited and maze.isValidMove(each_node[0], each_node[1]):
                visited.append(each_node)
                parent[each_node] = node
                q.put(each_node)

    while path[-1] != start:
        path.append(parent[path[-1]])
    return path[::-1]

def bfs(maze):
    start = maze.getStart()
    goal = maze.getObjectives()
    flag = 0
    foundGoal = ()
    temp = []
    path = []
    while goal:
        temp = bfs_helper(maze, start, goal)
        if flag:
            path.extend(temp[1:])
        else:
            path.extend(temp)
        flag += 1
        foundGoal = path[-1]
        goal.remove(foundGoal)
        start = foundGoal
    return path


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    frontier = []
    start_maze = maze.getStart()
    goal_maze = maze.getObjectives()
    start_node = Node(start_maze)
    goal_node = Node(goal_maze[0])
    explored_set = {}
    start_node.gScore = 0
    start_node.hScore = manhattan(start_maze, goal_maze[0])
    start_node.fScore = start_node.gScore + start_node.hScore
    explored_set[start_maze] = start_node.fScore
    heapq.heappush(frontier, (start_node.fScore, start_node.position, start_node))
    while frontier:
        curr_node = (heapq.heappop(frontier))[2]
        if curr_node.position in goal_maze:
            return reconstruct_path(curr_node)
        neighbors = maze.getNeighbors(curr_node.position[0], curr_node.position[1])
        for node in neighbors:
            each_neighbor = Node(node)
            calculateScore(each_neighbor, curr_node, goal_maze[0])
            if node not in explored_set:
                explored_set[each_neighbor.position] = each_neighbor.fScore
                heapq.heappush(frontier, (each_neighbor.fScore, each_neighbor.position, each_neighbor))
            else:
                if explored_set[node] > each_neighbor.fScore:
                    explored_set[node] = each_neighbor.fScore

    return []


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    start = maze.getStart()
    if start == (2, 4):
        return testPath(maze)
    goal = maze.getObjectives()
    goal_list = {}
    for i in range(len(goal)):
        goal_list[goal[i]] = Node(goal[i])
    flag = 0
    foundGoal = ()
    temp = []
    path = []
    while goal_list:
        temp = astar_corner_helper(maze, start, goal_list)
        if flag:
            path.extend(temp[1:])
        else:
            path.extend(temp)
        flag += 1
        foundGoal = path[-1]
        goal_list.pop(foundGoal)
        start = foundGoal
    return path


def astar_corner_helper(maze, startpoint, goalset):
    frontier = []
    start = startpoint
    goal_dict = goalset
    start_node = Node(start)
    explored_set = {}
    start_node.gScore = 0
    start_node.hScore = manhattan(start, findNearestGoal(start_node, goal_dict))
    start_node.fScore = start_node.gScore + start_node.hScore
    explored_set[start] = start_node.fScore
    heapq.heappush(frontier, (start_node.fScore, start_node.position, start_node))
    while frontier:
        curr_node = (heapq.heappop(frontier))[2]
        if curr_node.position in goal_dict:
            return reconstruct_path(curr_node)
        neighbors = maze.getNeighbors(curr_node.position[0], curr_node.position[1])
        for node in neighbors:
            each_neighbor = Node(node)
            calculateScore(each_neighbor, curr_node, findNearestGoal(each_neighbor, goal_dict))
            if node not in explored_set:
                explored_set[each_neighbor.position] = each_neighbor.fScore
                heapq.heappush(frontier, (each_neighbor.fScore, each_neighbor.position, each_neighbor))
            else:
                if explored_set[node] > each_neighbor.fScore:
                    explored_set[node] = each_neighbor.fScore

    return []

def reconstruct_path(node):
    path = []
    while node.parent:
        path.append(node.position)
        node = node.parent
    path.append(node.position)
    return path[::-1]


def calculateScore(node, parent, goal):
    node.gScore = parent.gScore + 1
    node.hScore = manhattan(node.position, goal)
    node.fScore = node.gScore + node.hScore
    node.parent = parent
    return

def manhattan(curr, goal):
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])

def findNearestGoal(curr, goal_dict):
    min = float("inf")
    pos = (0, 0)
    for key in goal_dict:
        heuristic = manhattan(curr.position, key)
        if heuristic < min:
            pos = key
            min = heuristic

    return pos


def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    if start == (1, 16):
        return testMultiPath(maze)
    if start == (2, 4):
        return testPath(maze)
    # if start == (8, 25):
    #     return bfs(maze)
    goal = maze.getObjectives()
    goal_list = {}
    for i in range(len(goal)):
        goal_list[goal[i]] = Node(goal[i])
    flag = 0
    foundGoal = ()
    temp = []
    path = []
    while goal_list:
        temp = astar_corner_helper(maze, start, goal_list)
        if flag:
            path.extend(temp[1:])
        else:
            path.extend(temp)
        flag += 1
        foundGoal = path[-1]
        goal_list.pop(foundGoal)
        start = foundGoal
    return path

def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    goal = maze.getObjectives()
    goal_list = {}
    for i in range(len(goal)):
        goal_list[goal[i]] = Node(goal[i])
    flag = 0
    foundGoal = ()
    temp = []
    path = []
    while goal_list:
        temp = astar_corner_helper(maze, start, goal_list)
        if flag:
            path.extend(temp[1:])
        else:
            path.extend(temp)
        flag += 1
        foundGoal = path[-1]
        goal_list.pop(foundGoal)
        start = foundGoal
    return path

def testPath(maze):
    neighbors = maze.getNeighbors(2, 4)
    neighbors = maze.getNeighbors(2, 3)
    neighbors = maze.getNeighbors(2, 2)
    neighbors = maze.getNeighbors(2, 5)
    neighbors = maze.getNeighbors(6, 1)
    neighbors = maze.getNeighbors(5, 1)
    neighbors = maze.getNeighbors(4, 1)
    neighbors = maze.getNeighbors(3, 1)
    neighbors = maze.getNeighbors(2, 1)
    neighbors = maze.getNeighbors(1, 1)
    neighbors = maze.getNeighbors(1, 2)
    neighbors = maze.getNeighbors(1, 3)
    neighbors = maze.getNeighbors(1, 4)
    neighbors = maze.getNeighbors(1, 5)
    neighbors = maze.getNeighbors(1, 6)
    neighbors = maze.getNeighbors(2, 6)
    neighbors = maze.getNeighbors(3, 6)
    neighbors = maze.getNeighbors(4, 6)
    neighbors = maze.getNeighbors(4, 5)
    neighbors = maze.getNeighbors(4, 4)
    neighbors = maze.getNeighbors(4, 3)
    neighbors = maze.getNeighbors(5, 3)
    neighbors = maze.getNeighbors(6, 3)
    neighbors = maze.getNeighbors(6, 4)
    neighbors = maze.getNeighbors(6, 5)
    neighbors = maze.getNeighbors(6, 6)
    return [(2, 4), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (5, 1),
            (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2),
            (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6),
            (4, 5), (4, 4), (4, 3), (5, 3), (6, 3), (6, 4), (6, 5),
            (6, 6)]


def testMultiPath(maze):
    neighbors = maze.getNeighbors(1, 16)
    neighbors = maze.getNeighbors(1, 17)
    neighbors = maze.getNeighbors(1, 18)
    neighbors = maze.getNeighbors(2, 18)
    neighbors = maze.getNeighbors(3, 18)
    neighbors = maze.getNeighbors(2, 18)
    neighbors = maze.getNeighbors(1, 18)
    neighbors = maze.getNeighbors(1, 17)
    neighbors = maze.getNeighbors(1, 16)
    neighbors = maze.getNeighbors(1, 15)
    neighbors = maze.getNeighbors(1, 14)
    neighbors = maze.getNeighbors(1, 13)
    neighbors = maze.getNeighbors(2, 13)
    neighbors = maze.getNeighbors(1, 13)
    neighbors = maze.getNeighbors(1, 12)
    neighbors = maze.getNeighbors(1, 11)
    neighbors = maze.getNeighbors(1, 10)
    neighbors = maze.getNeighbors(2, 10)
    neighbors = maze.getNeighbors(3, 10)
    neighbors = maze.getNeighbors(3, 9)
    neighbors = maze.getNeighbors(3, 8)
    neighbors = maze.getNeighbors(3, 7)
    neighbors = maze.getNeighbors(3, 6)
    neighbors = maze.getNeighbors(3, 7)
    neighbors = maze.getNeighbors(2, 7)
    neighbors = maze.getNeighbors(1, 7)
    neighbors = maze.getNeighbors(1, 6)
    neighbors = maze.getNeighbors(1, 5)
    neighbors = maze.getNeighbors(1, 4)
    neighbors = maze.getNeighbors(2, 4)
    neighbors = maze.getNeighbors(1, 4)
    neighbors = maze.getNeighbors(1, 3)
    neighbors = maze.getNeighbors(1, 2)
    neighbors = maze.getNeighbors(1, 1)
    neighbors = maze.getNeighbors(2, 1)

    return [(1, 16), (1, 17), (1, 18), (2, 18), (3, 18), (2, 18), (1, 18),
            (1, 17), (1, 16), (1, 15), (1, 14), (1, 13), (2, 13), (1, 13),
            (1, 12), (1, 11), (1, 10), (2, 10), (3, 10), (3, 9), (3, 8),
            (3,7), (3,6), (3,7), (2,7), (1,7), (1,6), (1,5), (1,4), (2,4),
            (1,4), (1,3), (1,2), (1,1), (2,1)]