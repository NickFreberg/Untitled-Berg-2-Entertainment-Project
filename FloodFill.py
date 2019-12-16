from array import *

# map derived from Outdoors.tmx layer "Extra Walls"
MAP = [[1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,0,0,0,0, 0,0,0,0,1, 1,0,0,0,0, 0,0,0,0,1],
       [1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1]]




def print_map(map):
       mapWidth =len(map)
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


floodFill(MAP, 1, 1, 0, 2)
#print(floodFill(MAP, 1, 1, 0, 2))
#print(len(MAP[2]))
print_map(MAP)

