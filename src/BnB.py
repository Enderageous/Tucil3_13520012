import os
import random
import time
from heapq import heappush, heappop
from tokenize import Token


# Class for priority queue
class PQueue:

    # Initiate a Priority Queue
    def __init__(self):
        self.heap = []

    # Push into the queue
    def push(self, k):
        heappush(self.heap, k)

    # Pop from the queue
    def pop(self):
        return heappop(self.heap)

    # Check if the queue is empty
    def empty(self):
        if not self.heap:
            return True
        else:
            return False

# Class for nodes
class Node:

    # Initiate a node
    def __init__(self, cost, level, parent, puzzle, move):
        self.cost = cost
        self.level = level
        self.parent = parent
        self.puzzle = puzzle
        self.move = move

    # overide the function Less Than (<) for the priority queue
    def __lt__(self, nxt):
        return self.cost + self.level < nxt.cost + nxt.level

# Function for reading files
def readFile():
    puzzle = []
    puzzleRow = []

    filename = input("Please input filename: ")
    path = os.path.join((os.path.abspath(os.path.join(os.getcwd(), os.pardir))), "test", filename)
    while (not os.path.exists(path)):
        filename = input("\nFilename not found. Please reinput filename: ")
        path = os.path.join((os.path.abspath(os.path.join(os.getcwd(), os.pardir))), "test", filename)
    
    file = open(path).read()
    array = file.split('\n')
    for i in range (len(array)):
        elements = array[i].split(" ")
        puzzleRow = []
        for j in range (len(elements)):
            puzzleRow.append(int(elements[j]))
        puzzle.append(puzzleRow)
    
    return (puzzle)

# Function to randomized a puzzle
def randomPuzzle():
    puzzle = []
    puzzleRow = []
    check = [False for i in range (16)]
    
    for i in range (4):
        puzzleRow = []
        for j in range(4):
            n = random.randint(1,16)
            while (check[n-1]):
                n = random.randint(1,16) 
            check[n-1] = True
            puzzleRow.append(n)
        puzzle.append(puzzleRow)
    
    return (puzzle)

# Function that counts KURANG(i) + X
def kurang(puzzle) :
    kurang = 0
    before = 0
    print("KURANG(i):")
    for e in range(1, len(puzzle) * len(puzzle[0]) + 1):
        found = False
        grid = False
        ii = 0
        jj = 0
        while (ii < len(puzzle) and not found):
            jj=0
            while (jj < len(puzzle[0]) and not found):
                if (puzzle[ii][jj] == e):
                    found = True
                else:
                    jj += 1
            if (not found):
                ii += 1
        for i in range (len(puzzle)):
            for j in range (len(puzzle[i])):
                if (puzzle[i][j] < e and ((i > ii) or (i == ii and j > jj))) :
                    kurang += 1
                if (e == 16 and puzzle[i][j] == 16 and ((i%2 == 1 and j%2 == 0) or (i%2 == 0 and j%2 == 1))):
                    kurang += 1
                    grid = True
        if (grid):
            print("Tile " + str(e) + ": " + str(kurang - before - 1))
            before = kurang
        else:
            print("Tile " + str(e) + ": " + str(kurang - before))
            before = kurang
    
    return kurang

# Function that prints out the puzzle and KURANG(i) + X
def printPuzzleKurang(puzzle):

    print("Puzzle:")
    x = '\n'.join([''.join(['{:4}'.format(element) for element in row]) for row in puzzle])
    print(x)

    print("")
    nkurang = kurang(puzzle)
    print("\nKURANG(i) + X =", nkurang,"\n")

    return nkurang


# Function that counts how many tiles are not in the correct places
def countWrong(puzzle):
    cost = 0

    for i in range (len(puzzle)):
        for j in range (len(puzzle[0])):
            if (puzzle[i][j] != (i*len(puzzle[0]) + j + 1)):
                cost += 1
    return (cost)

# Function that search the location of the empty tile (16 tile)
def search16(puzzle):
    i = 0
    j = 0
    found = False

    while (i < len(puzzle) and not found):
        j = 0
        while (j < len(puzzle[0]) and not found):
            if (puzzle[i][j] == 16):
                found = True
            else:
                j += 1
        if (not found):
            i += 1
    
    return ([i, j])
    
# Function that switch a tile with an empty tile
def switchEmpty(puzzle, i, j):
    empty = search16(puzzle)
    tileSwitched = [empty[0] + i, empty[1] + j]
    temp = puzzle[empty[0]][empty[1]]
    puzzle[empty[0]][empty[1]] = puzzle[tileSwitched[0]][tileSwitched[1]]
    puzzle[tileSwitched[0]][tileSwitched[1]] = temp
    
    return (puzzle)

# Function that prints out the puzzle movements from start to finish
def printFinal(node):
    i = 0

    if (node.parent != None):
        i = printFinal(node.parent)
        i += 1

    print("Puzzle move " + str(i) + ": " )
    x = '\n'.join([''.join(['{:4}'.format(element) for element in row]) for row in node.puzzle])
    print(x, "\n")

    return (i)

# Function that checks if a move is the reverse of the move before that
def notReverse(i, j):
    return (not((i == 0 and j == 2) or (i == 2 and j == 0) or (i == 1 and j == 3) or (i == 3 and j == 1)))

# Procedure that solves the puzzle with Branch and Bound
def solve(puzzle):
    startTimer = time.perf_counter()

    finalPuzzle = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    rowMove = [ 1, 0, -1, 0 ]  # Empty slot move 0 = down, 1 = left, 2 = up, 3 = right
    colMove = [ 0, -1, 0, 1 ]
    pqueue = PQueue()
    totalNodes = 1
    
    # Make root node
    root = Node(countWrong(puzzle), 0, None, puzzle, None)
    pqueue.push(root)

    # Gets node with the lowest cost
    while (not pqueue.empty()):
        pnode = pqueue.pop()
        current = pnode.puzzle
        if (current == finalPuzzle):
            break
        else:
            # Move the empty tile to 4 different ways
            for i in range (4):
                empty = search16(current)
                # Check if move is valid
                if (empty[0] + rowMove[i] >= 0 and empty[0] + rowMove[i] < len(current) and empty[1] + colMove[i] >= 0 and empty[1] + colMove[i] < len(current[0]) and notReverse(i, pnode.move)):
                    # Make the moved puzzle
                    switchedPuzzle = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
                    for ii in range (len(current)):
                        for jj in range (len(current[0])):
                            switchedPuzzle[ii][jj] = current[ii][jj]
                    switchedPuzzle = switchEmpty(switchedPuzzle, rowMove[i], colMove[i])
                    # Make the node and push it to priority queue
                    child = Node(countWrong(switchedPuzzle), pnode.level + 1, pnode, switchedPuzzle, i)
                    pqueue.push(child)
                    totalNodes += 1
    
    endTimer = time.perf_counter()
    printFinal(pnode)
    print(totalNodes, "nodes were created in the algorithm")
    print(f"The elapsed time is {endTimer - startTimer:0.4f} seconds")
    print("")