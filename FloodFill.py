from array import *


class Node():
    def __init__(self, x_coord: int, y_coord:int):
        self.weight = None
        self.x = x_coord
        self.y = y_coord
        self.up: Node = None
        self.down: Node = None
        self.left: Node = None
        self.right: Node = None


    def print_node(self):
        print(str(self.x) + ", " + str(self.y))




# map derived from 4Rooms.tmx layer "WALLS"

MAP = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


"""
def build_node_weights(wall):
    i=0
    j=0
    ground = [[]]
    mapWidth = len(wall)
    print("mapWidth: ", mapWidth)
    mapHeight = len(wall[0])
    print("mapHeight: ", mapHeight)
    # for every row in the array
    for row in range(mapWidth):
        # for every tile in this row
        for col in range(mapHeight):
            x = ground[col][row]
            y = ground[col][row]
            print("x = ", x + ", y = ", y)
            # if the tile isnt free (i.e. is a wall)
            if y != 0:
                # set the weight to 1000
                ground[col][row] = 1000
        return ground
"""
"""
def build_node_arr(weights):
    big_arr = []
    u = None
    d = None
    l = None
    r = None

    # we need to make 20 nodes per row
    for thing in range(20):
        #do it one row at a time and then append the entire row to the big array
        row = []
        for j in range(20):
            #node creation
            # will have to add logic to change the up down left and right to connect the nodes
            new_node = Node(weights[thing][j], u, d, l, r)
            #add the new node to the row
            row.append(new_node)
    # at the end of it all we should have a beautiful 20x20 array
    return big_arr
"""


def print_map(map):
    mapWidth = len(map)
    mapHeight = len(map[0])

    for row in range(mapHeight):
        for col in range(mapWidth):
            print(map[col][row])
        print()


def floodFill(world, x, y, oldChar, newChar):
    # The recursive algorithm. Starting at x and y, changes any adjacent
    # characters that match oldChar to newChar.
    worldWidth = len(world)
    worldHeight = len(world[0])

    if oldChar == None:
        oldChar = world[x][y]

    if world[x][y] != oldChar:
        # Base case. If the current x, y character is not the oldChar,
        # then do nothing.
        return

    # Change the character at world[x][y] to newChar
    world[x][y] = newChar

    # Recursive calls. Make a recursive call as long as we are not on the
    # boundary (which would cause an Index Error.)
    if x > 0: # left
        floodFill(world, x-1, y, oldChar, newChar)

    if y > 0: # up
        floodFill(world, x, y-1, oldChar, newChar)

    if x < worldWidth-1: # right
        floodFill(world, x+1, y, oldChar, newChar)

    if y < worldHeight-1: # down
        floodFill(world, x, y+1, oldChar, newChar)


def getNumOfRooms(world):
    worldWidth = len(world)
    worldHeight = len(world[0])

    roomCount = 0

    for x in range(worldWidth):
        for y in range(worldHeight):
            # on each possible x, y empty space in the map, call floodfill.
            if world[x][y] == 0:
                floodFill(world, x, y, 0, 'x')

                # comment out the next two lines if you don't want
                # getNumOfRooms() to display output when called.
                print_map(world)
                print()

                roomCount += 1
    return roomCount


myNode = Node(3,2)
myNode.print_node()
floodFill(MAP, 1, 1, 0, 2)
print(MAP)



#node_arr = build_node_arr(test_build)
