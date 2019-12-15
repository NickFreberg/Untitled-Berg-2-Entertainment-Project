from array import *

# map derived from Outdoors.tmx layer "Extra Walls"
MAP = [[0,0,0,0,0, 1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0],
       [0,0,0,0,0, 1,1,1,1,1, 1,1,1,1,1, 0,0,0,0,0],
       [0,0,0,0,0, 0,0,1,0,0, 0,0,1,0,0, 0,0,0,0,0],
       [0,0,0,0,0, 0,0,1,0,0, 0,0,1,0,0, 0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,179,185,156,185,185,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,164,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,159,159,159,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [579,579,579,579,579,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [579,579,579,579,579,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [579,579,579,579,579,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [579,579,579,579,579,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [579,579,579,579,579,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,661,451,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [1,1,1,1,1, 1,1,1,0,0, 0,0,0,0,0, 0,0,0,0,0],
       [1,1,1,1,1, 1,1,1,0,0, 0,0,0,0,0, 0,0,0,0,0]]

print(len(MAP[2]))


def print_map():
    for row in MAP:
        for col in row:
            print(col, end=" ")
        print()

print_map()