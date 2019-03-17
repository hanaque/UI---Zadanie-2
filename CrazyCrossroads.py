import json
from copy import copy, deepcopy


def calculateDFS(Cars, CrossroadsSize):

    """
    :param Cars: Initial state of crossroads
    :param CrossroadsSize: Size of crossroads
    :return: Function returns string with moves from begin to end

    level indicates how deep am I with moves, so level == 11 means i did 11 moves so far
    stateIndex indicates index of node in current level
    Every node has following attributes:
        "state": Cars, - current state of cars in crossroads
        "move": None, - move made
        "parent": -1, - index of parent node
        "color": None, - color of car
        "childindexes": [], - list of child indexes (e.g. 4,5,6)
        "childlooked": -1  - index of child in childindexes i am looking at right now
    """

    level = 0
    stateIndex = 0

    root = {
        "state": Cars,
        "move": None,
        "parent": -1,
        "color": None,
        "childindexes": [],
        "childlooked": -1
    }

    #I am using 2d array, where each node is using python dictionary
    states = [[]]
    states.append([])

    #I initialize root
    states[0].append(root)

    #this list indicates if i allocated row in given level
    levels_in_list = []
    levels_in_list.append(level)
   # print(levels_in_list)


    while True:

        #If i didnt allocated memory in level do it now
        if (level + 1) not in levels_in_list:
            levels_in_list.append(level + 1)
            states.append([])

        #Dictionaries are hard to index so i am using auxilary variable as indexof cars
        carIndex = 0

        #Iterate through each car and add all posible moves
        for car in states[level][stateIndex]["state"]:

            #It is illegal to move with car i moved last turn
            if car["color"] == states[level][stateIndex]["color"]:
                carIndex += 1
                continue

            #If car is horizontal I am checking left and right moves
            if car["side"] == 'h':

                #I can move 1 to Index of car steps
                for i in range(1, int(car["Y"])):

                    #I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                    if MoveableLeft(car, i, states[level][stateIndex]["state"]):

                        #I copy state and make needed move happen
                        newState = deepcopy(states[level][stateIndex]["state"])
                        newState[carIndex]["Y"] = int(newState[carIndex]["Y"]) - i

                        #I check if move i made is loop
                        if DetectCycles(level, stateIndex, newState, states):
                            newMove = "VLAVO(" + car["color"] + ", " + str(i) + ")"

                            #Define node
                            newNode = {
                                "state": newState,
                                "move": newMove,
                                "parent": stateIndex,
                                "color": car["color"],
                                "childindexes": [],
                                "childlooked": -1
                            }

                            #I add child index to current node
                            states[level][stateIndex]["childindexes"].append(len(states[level + 1]))
                            #Add state to array
                            states[level + 1].append(newNode)

                #I can move (SizeOf Maze - location of car) steps max
                for i in range(1, int(CrossroadsSize["Y"]) - int(car["Y"])):

                    # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                    if MoveableRight(car, i, states[level][stateIndex]["state"]):

                        # I copy state and make needed move happen
                        newState = deepcopy(states[level][stateIndex]["state"])
                        newState[carIndex]["Y"] = int(newState[carIndex]["Y"]) + i

                        # I check if move i made is loop
                        if DetectCycles(level, stateIndex, newState, states):
                            newMove = "VPRAVO(" + car["color"] + ", " + str(i) + ")"

                            #Define node
                            newNode = {
                                "state": newState,
                                "move": newMove,
                                "parent": stateIndex,
                                "color": car["color"],
                                "childindexes": [],
                                "childlooked": -1
                            }

                            #I add child index to current node
                            states[level][stateIndex]["childindexes"].append(len(states[level + 1]))
                            #Add state to array
                            states[level + 1].append(newNode)

                            #If i moved RED car to the rightest position, i solved a problem and return path
                            if car["color"] == "cervene":
                                if int(newState[carIndex]["Y"]) + int(newState[carIndex]["size"]) - 1 == int(CrossroadsSize["Y"]):
                                    return return_path(level, stateIndex, newNode, states)

            #If car is vertical, i am checking up and down
            else:
                # I can move 1 to Index of car steps
                for i in range(1, int(car["X"])):
                    # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                    if MoveableUp(car, i, states[level][stateIndex]["state"]):

                        # I copy state and make needed move happen
                        newState = deepcopy(states[level][stateIndex]["state"])
                        newState[carIndex]["X"] = int(newState[carIndex]["X"]) - i

                        # I check if move i made is loop
                        if DetectCycles(level, stateIndex, newState, states):
                            newMove = "HORE(" + car["color"] + ", " + str(i) + ")"

                            # Define node
                            newNode = {
                                "state": newState,
                                "move": newMove,
                                "parent": stateIndex,
                                "color": car["color"],
                                "childindexes": [],
                                "childlooked": -1
                            }

                            # I add child index to current node
                            states[level][stateIndex]["childindexes"].append(len(states[level + 1]))
                            # Add state to array
                            states[level + 1].append(newNode)

                # I can move (SizeOf Maze - location of car) steps max
                for i in range(1, int(CrossroadsSize["X"]) - int(car["X"])):
                    # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                    if MoveableDown(car, i, states[level][stateIndex]["state"]):

                        # I copy state and make needed move happen
                        newState = deepcopy(states[level][stateIndex]["state"])
                        newState[carIndex]["X"] = int(newState[carIndex]["X"]) + i

                        # I check if move i made is loop
                        if DetectCycles(level, stateIndex, newState, states):
                            newMove = "DOLE(" + car["color"] + ", " + str(i) + ")"

                            # Define node
                            newNode = {
                                "state": newState,
                                "move": newMove,
                                "parent": stateIndex,
                                "color": car["color"],
                                "childindexes": [],
                                "childlooked": -1
                            }

                            # I add child index to current node
                            states[level][stateIndex]["childindexes"].append(len(states[level + 1]))
                            # Add state to array
                            states[level + 1].append(newNode)

            #looping next car, increment index
            carIndex += 1

        #If there is any child left to be processed I am going to process it (else: part)
        #Otherwise i am going to loop back and find childs there. (if: part)
        if len(states[level][stateIndex]["childindexes"]) <= states[level][stateIndex]["childlooked"] + 1:

            #Get parent index and decrement level
            parent_index = states[level][stateIndex]["parent"]
            level -= 1

            #While i didnt reach bottom node i loop back
            while level >= 0:

                #Get number of child and increment visiting index of childs
                num_of_childs = len(states[level][parent_index]["childindexes"])
                states[level][parent_index]["childlooked"] = int(states[level][parent_index]["childlooked"]) + 1

                #If there are unvisited childs visit it and break
                #Else loopback to parent
                if num_of_childs > states[level][parent_index]["childlooked"]:
                    #Set current index and increment level to given child
                    stateIndex = states[level][parent_index]["childlooked"]
                    level += 1
                    break
                else:
                    #loop parent
                    parent_index = states[level][parent_index]["parent"]
                    level -= 1

            #If i get to negative level i did not find suitable solution
            if level < 0:
                return "No solution found"

        else:
            #Process next unvisited child
            states[level][stateIndex]["childlooked"] = int(states[level][stateIndex]["childlooked"]) + 1
            tmp = states[level][stateIndex]["childlooked"]
            stateIndex = tmp
            level += 1



    return 0


def calculateBFS(Cars, CrossroadsSize):

    """
    :param Cars: Initial state of crossroads
    :param CrossroadsSize: Size of crossroads
    :return: Function returns string with moves from begin to end

    level indicates how deep am I with moves, so level == 11 means i did 11 moves so far
    stateIndex indicates index of node in current level
    Every node has following attributes:
        "state": Cars, - current state of cars in crossroads
        "move": None, - move made
        "parent": -1, - index of parent node
        "color": None, - color of car
        In bfs i will not loopback to childs, because i will process them all at once
    """

    level = 0
    root = {
        "state" : Cars,
        "move" : None,
        "parent" : -1,
        "color" : None
    }

    # Flag that set to True when there was added move
    wasmoved = True

    # I am using 2d array, where each node is using python dictionary
    states = [[]]
    states.append([])

    # Initialize root
    states[0].append(root)

    while True:
        # If there was no move in given level algorithm ends with no solution
        if wasmoved == False:
            return "No solution found"

        # Set flag
        wasmoved = False

        # Expand array
        states.append([])

        #Initialize index
        stateIndex = 0

        #For each state in given level i check moves
        for state in (states[level]):

            # Initialize index of cars
            carIndex = 0

            #For each car i check posible moves
            for car in state["state"]:

                # I is illegal to process same car 2 times in a row
                if car["color"] == state["color"]:
                    carIndex += 1
                    continue

                # If car is horizontal i check left and right moves
                if car["side"] == 'h':

                    # I can move 1 to Index of car steps
                    for i in range(1, int(car["Y"])):
                        # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                        if MoveableLeft(car, i, state["state"]):

                            # I copy state and make needed move happen
                            newState = deepcopy(state["state"])
                            newState[carIndex]["Y"] = int(newState[carIndex]["Y"]) - i

                            # I check if move i made is loop
                            if DetectCycles(level, stateIndex, newState, states):
                                newMove = "VLAVO(" + car["color"] + ", " + str(i) + ")"

                                # Define node
                                newNode = {
                                    "state": newState,
                                    "move": newMove,
                                    "parent": stateIndex,
                                    "color": car["color"]
                                }

                                # I append node to array
                                states[level + 1].append(newNode)

                                # set flag
                                wasmoved = True

                    # I can move (SizeOf Maze - location of car) steps max
                    for i in range(1, int(CrossroadsSize["Y"]) - int(car["Y"])):

                        # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                        if MoveableRight(car, i, state["state"]):

                            # I copy state and make needed move happen
                            newState = deepcopy(state["state"])
                            newState[carIndex]["Y"] = int(newState[carIndex]["Y"]) + i

                            # I check if move i made is loop
                            if DetectCycles(level, stateIndex, newState, states):
                                newMove = "VPRAVO(" + car["color"] + ", " + str(i) + ")"

                                # Define node
                                newNode = {
                                    "state": newState,
                                    "move": newMove,
                                    "parent": stateIndex,
                                    "color": car["color"]
                                }

                                # I append node to array
                                states[level + 1].append(newNode)

                                # Set flag
                                wasmoved = True

                                # If RED car is in final state i solved problem and return MOVES
                                if car["color"] == "cervene":
                                    if int(newState[carIndex]["Y"]) + int(newState[carIndex]["size"]) - 1 == int(CrossroadsSize["Y"]):
                                        return return_path(level, stateIndex, newNode , states)

                else:
                    # I can move 1 to Index of car steps
                    for i in range(1, int(car["X"])):

                        # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                        if MoveableUp(car, i, state["state"]):

                            # I copy state and make needed move happen
                            newState = deepcopy(state["state"])
                            newState[carIndex]["X"] = int(newState[carIndex]["X"]) - i

                            # I check if move i made is loop
                            if DetectCycles(level, stateIndex, newState, states):
                                newMove = "HORE(" + car["color"] + ", " + str(i) + ")"

                                # Define node
                                newNode = {
                                    "state": newState,
                                    "move": newMove,
                                    "parent": stateIndex,
                                    "color": car["color"]
                                }

                                # Append node to array and set flag
                                states[level + 1].append(newNode)
                                wasmoved = True

                    # I can move (SizeOf Maze - location of car) steps max
                    for i in range(1, int(CrossroadsSize["X"]) - int(car["X"])):

                        # I call function which tells me if move is legal, i pass car, number of moves and state of crossroads
                        if MoveableDown(car, i, state["state"]):

                            # I copy state and make needed move happen
                            newState = deepcopy(state["state"])
                            newState[carIndex]["X"] = int(newState[carIndex]["X"]) + i

                            # I check if move i made is loop
                            if DetectCycles(level, stateIndex, newState, states):
                                newMove = "DOLE(" + car["color"] + ", " + str(i) + ")"

                                # Define node
                                newNode = {
                                    "state": newState,
                                    "move": newMove,
                                    "parent": stateIndex,
                                    "color": car["color"]
                                }

                                states[level + 1].append(newNode)
                                wasmoved = True
                                #print(newMove)

                carIndex += 1
            stateIndex += 1
        level += 1


#Function that reconstructs moves used in solution
def return_path(level, index, state, states):

    #Set first move
    solution_path = state["move"]

    # Looping thought nodes and appending moves
    while level != 0:
        solution_path = states[level][index]["move"] + ", " + solution_path
        index = states[level][index]["parent"]
        level -= 1

    #Returns solution in string
    return solution_path

#Important function that detects cycles
def DetectCycles(level, index, state, states):

    #Looping parents and checking if state of crossroads is same, if yes return false otherwise loop to parent until at root node
    while level != -1:
        if states[level][index]["state"] == state:
            return False
        else:
            index = states[level][index]["parent"]
            level -= 1

    return True

#DetectsCycles in all nodes, not used because of uneffiency
def DetectCycles_ALLNODES(level, index, state, states):

    #Looping parents and checking if state of crossroads is same, if yes return false otherwise loop to parent until at root node
    while level != -1:
        for node in states[level]:
            if node["state"] == state:
                return False
        level -= 1

    return True

#Function that checks if car is moveable 'steps' right
def MoveableRight(car, steps, Cars):
    if int(car["Y"]) + int(car["size"]) - 1 + steps <= int(CrossroadsSize["Y"]):
        startPoint = int(car["Y"]) + int(car["size"])
        for i in range(steps):
            for c in Cars:
                if c["side"] == 'v':
                    if startPoint + i == int(c["Y"]):
                        for j in range(int(c["size"])):
                            if int(car["X"]) == int(c["X"]) + j:
                                return False
                else:
                    if car["X"] == c["X"]:
                        for j in range(int(c["size"])):
                            if startPoint + i == int(c["Y"]) + j:
                                return False
    else:
        return False

    return True

#Function that checks if car is moveable 'steps' left
def MoveableLeft(car, steps, Cars):
    if int(car["Y"]) - steps > 0:
        startPoint = int(car["Y"]) - 1
        for i in range(steps):
            for c in Cars:
                if c["side"] == 'v':
                    if startPoint - i == int(c["Y"]):
                        for j in range(int(c["size"])):
                            if int(car["X"]) == int(c["X"]) + j:
                                return False
                else:
                    if car["X"] == c["X"]:
                        for j in range(int(c["size"])):
                            if startPoint - i == int(c["Y"]) + j:
                                return False
    else:
        return False
    return True

#Function that checks if car is moveable 'steps' up
def MoveableUp(car, steps, Cars):
    if int(car["X"]) - steps > 0:
        startPoint = int(car["X"]) - 1
        for i in range(steps):
            for c in Cars:
                if c["side"] == 'h':
                    if startPoint - i == int(c["X"]):
                        for j in range(int(c["size"])):
                            if int(car["Y"]) == int(c["Y"]) + j:
                                return False
                else:
                    if car["Y"] == c["Y"]:
                        for j in range(int(c["size"])):
                            if startPoint - i == int(c["X"]) + j:
                                return False
    else:
        return False
    return True

#Function that checks if car is moveable 'steps' down
def MoveableDown(car, steps, Cars):
    if int(car["X"]) + int(car["size"]) - 1 + steps <= int(CrossroadsSize["X"]):
        startPoint = int(car["X"]) + int(car["size"])
        for i in range(steps):
            for c in Cars:
                if c["side"] == 'h':
                    if startPoint + i == int(c["X"]):
                        for j in range(int(c["size"])):
                            if int(car["Y"]) == (int(c["Y"]) + j):
                                return False
                else:
                    if car["Y"] == c["Y"]:
                        for j in range(int(c["size"])):
                            if startPoint + i == int(c["X"]) + j:
                                return False
    else:
        return False
    return True



#Set input files
crossroads_size = input('Enter file with sizes(e.g CrossroadsSize.json): ')
crossroads_state = input('Enter file with state of croosroads(e.g Cars.json): ')

#Open files and get values
with open(crossroads_size) as Size:
    CrossroadsSize = json.load(Size)

with open(crossroads_state) as Car:
    Cars = json.load(Car)

#print(MoveableDown(Cars[2], 1, Cars))

#Calculate problem with DFS and BFS and compare results
solutionDFS = calculateDFS(Cars,CrossroadsSize)
solutionBFS = calculateBFS(Cars,CrossroadsSize)
print("DFS output: ", solutionDFS)
print("BFS output: ", solutionBFS)

#Case no solution print it and exit with 1
if solutionBFS == "No solution found" or solutionDFS == "No solution found":
    exit(1)

#Tokenize result string to get number of moves
numofmovesBFS = len(solutionBFS.split("),"))
numofmovesDFS = len(solutionDFS.split("),"))

#Print better result
if numofmovesBFS < numofmovesDFS:
    print("Path return from BFS is better, ", numofmovesBFS, " moves only")
else:
    print("Path return from DFS is better, ", numofmovesDFS, " moves only")

#exit with 0
exit(0)