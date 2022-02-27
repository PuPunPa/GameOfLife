"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import os.path

ON = 1
OFF = 0
vals = [ON, OFF]

#Structures
#Stills
block = np.array([[ON, ON],
                  [ON, ON]])

beehive = np.array([[OFF, ON,  ON,  OFF],
                    [ON,  OFF, OFF, ON],
                    [OFF, ON,  ON,  OFF]])

loaf = np.array([[OFF, ON,  ON,  OFF],
                 [ON,  OFF, OFF, ON],
                 [OFF, ON,  OFF, ON],
                 [OFF, OFF, ON,  OFF]])

boat = np.array([[ON,  ON,  OFF],
                 [ON,  OFF, ON],
                 [OFF, ON,  OFF]])

tub = np.array([[OFF, ON,  OFF],
                [ON,  OFF, ON],
                [OFF, ON,  OFF]])

#Oscilators
blinkerA = np.array([[ON], 
                     [ON], 
                     [ON]])

blinkerB = np.array([[ON, ON, ON]])

toadA = np.array([[OFF, OFF, ON,  OFF],
                  [ON,  OFF, OFF, ON],
                  [ON,  OFF, OFF, ON],
                  [OFF, ON,  OFF, OFF]])

toadB = np.array([[OFF, ON, ON, ON],
                  [ON,  ON, ON, OFF]])

beaconA = np.array([[ON,  ON,  OFF, OFF],
                    [ON,  ON,  OFF, OFF],
                    [OFF, OFF, ON, ON],
                    [OFF, OFF, ON, ON]])

beaconB = np.array([[ON,  ON,  OFF, OFF],
                    [ON,  OFF, OFF, OFF],
                    [OFF, OFF, OFF, ON],
                    [OFF, OFF, ON,  ON]])

#Spaceships
gliderA = np.array([[OFF, ON,  OFF], 
                    [OFF, OFF, ON], 
                    [ON,  ON, ON]])

gliderB = np.array([[ON,  OFF, ON], 
                    [OFF, ON,  ON], 
                    [OFF, ON,  OFF]])

gliderC = np.array([[OFF, OFF, ON], 
                    [ON,  OFF, ON], 
                    [OFF, ON,  ON]])

gliderD = np.array([[ON,  OFF, OFF], 
                    [OFF, ON,  ON], 
                    [ON,  ON,  OFF]])

lwShipA = np.array([[ON,  OFF, OFF, ON,  OFF],
                    [OFF, OFF, OFF, OFF, ON],
                    [ON,  OFF, OFF, OFF, ON],
                    [OFF, ON,  ON,  ON,  ON]])

lwShipB = np.array([[OFF, OFF, ON,  ON,  OFF],
                    [ON,  ON,  OFF, ON,  ON],
                    [ON,  ON,  ON,  ON,  OFF],
                    [OFF, ON,  ON,  OFF, OFF]])

lwShipC = np.array([[OFF, ON,  ON,  ON,  ON],
                    [ON,  OFF, OFF, OFF, ON],
                    [OFF, OFF, OFF, OFF, ON],
                    [ON,  OFF, OFF, ON,  OFF]])

lwShipD = np.array([[OFF, ON,  ON,  OFF, OFF],
                    [ON,  ON,  ON,  ON,  OFF],
                    [ON,  ON,  OFF, ON,  ON],
                    [OFF, OFF, ON,  ON,  OFF]])

iteration = 0

entities = [block, beehive, loaf, tub, blinkerA, blinkerB, toadA, toadB, beaconA, beaconB, gliderA, gliderB, gliderC, gliderD, lwShipA, lwShipB, lwShipC, lwShipD]
entityName = ["block", "beehive", "loaf", "tub", "blinker", "blinker", "toad", "toad", "beacon", "beacon", "glider", "glider", "glider", "glider", "lwShip", "lwShip", "lwShip", "lwShip"]

def shave(grid):
    for i in range(4):
        grid = grid[~np.all(grid == 0, axis=1)]
        grid = np.rot90(grid)
    return grid

def findShape(grid):
    grid = shave(grid)
    for _ in range(4):
        print(grid)
        try :
            position = entities.index(grid)
            print(position)
            return entityName(position)
        except ValueError:
            grid = np.rot90(grid)
    return "none"

def growingZeros(grid):
    width, height = grid.shape
    neighbors = []
    #find candidates
    for j in range(height):
        for i in range(width):
            if grid[i][j] == OFF:
                up = grid[i][(j-1)%height]
                down = grid[i][(j+1)%height]
                left = grid[(i-1)%width][j]
                right = grid[(i+1)%width][j]
                if (up + down + left + right) < ON*2:
                    neighbors.append("%s %s" % (i, j))
    
    #flood fill
    while(len(neighbors) > 0):
        i, j = neighbors.pop(0).split(" ")
        i = int(i)
        j = int(j)
        #print("[%s, %s]" % (x, y))
        grid[i][j] = 2
        up = grid[i][(j-1)%height]
        down = grid[i][(j+1)%height]
        left = grid[(i-1)%width][j]
        right = grid[(i+1)%width][j]
        if up == OFF and ("%s %s" % (i, (j-1)%height)) not in neighbors:
            neighbors.append("%s %s" % (i, (j-1)%height))
        if down == OFF and ("%s %s" % (i, (j+1)%height)) not in neighbors:
            neighbors.append("%s %s" % (i, (j+1)%height))
        if left == OFF and ("%s %s" % ((i-1)%width, j)) not in neighbors:
            neighbors.append("%s %s" % ((i-1)%width, j))
        if right == OFF and ("%s %s" % ((i+1)%width, j)) not in neighbors:
            neighbors.append("%s %s" % ((i+1)%width, j))

    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in grid]))
    print("-----------------------------------------------------")
    return grid

def growingShapes(grid):
    width, height = grid.shape
    neighbors = []
    shapes = []
    for j in range(height):
        for i in range(width):
            if grid[i][j] < 2:
                shape = np.zeros(width*height).reshape(width, height)
                neighbors.append("%s %s" % (i, j))
                while(len(neighbors) > 0):
                    a, b = neighbors.pop(0).split(" ")
                    a = int(a)
                    b = int(b)
                    if grid[a][b] < 2:
                        shape[a][b] = grid[a][b]
                    grid[a][b] = 2
                    up = grid[a][(b-1)%height]
                    down = grid[a][(b+1)%height]
                    left = grid[(a-1)%width][b]
                    right = grid[(a+1)%width][b]
                    if up < 2:
                        neighbors.append("%s %s" % (a, (b-1)%height))
                    if down < 2:
                        neighbors.append("%s %s" % (a, (b+1)%height))
                    if left < 2:
                        neighbors.append("%s %s" % ((a-1)%width, b))
                    if right < 2:
                        neighbors.append("%s %s" % ((a+1)%width, b))
                shapes.append(shape)
    return shapes

def inputText(file):
    with open(file) as f:
        lines = f.readlines()
    
    width, height = lines[0].split(" ")
    print("[" + width + ", " + height[:-1] + "]")
    generations = int(lines[1])
    print(generations)

    grid = np.zeros((int(width), int(height)))
    for line in lines[2:]:
        print(line)
        x, y = line.split(" ")
        grid[int(x), int(y)] = ON
    return generations, grid

def randomGrid(N, M):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*M, p=[0.2, 0.8]).reshape(N, M)

def addStructure(i, j, grid, structure):
    """adds a structure with top left cell at (i, j)"""
    x, y = structure.shape
    grid[i:i+x, j:j+y] = structure

def neighbors(grid, i, j):
    width, height = grid.shape
    neighbors = 0
    for y in range (j-1, j+2):
        for x in range (i-1, i+2):
            if grid[x%width, y%height] == ON:
                neighbors += 1
    return neighbors - (grid[i, j]/ON)

def update(frameNum, img, grid):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    width, height = grid.shape
    for j in range(height):
        for i in range(width):
            neighborCount = neighbors(grid, i, j)
            
            #Starved or Overpopulated
            if grid[i, j] == ON:
                if neighborCount < 2 or neighborCount > 3:
                    newGrid[i, j] = OFF

            #Reproduces
            elif grid[i, j] == OFF and neighborCount == 3:
                newGrid[i, j] = ON

    # update data
    img.set_data(newGrid)
    global iteration
    print(iteration)
    iteration += 1
    analyze = growingZeros(grid)
    shapes = growingShapes(analyze)
    for shape in shapes:
        print(findShape(shape))
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    path = "input.txt"
        
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    frameCount = 0
    
    if os.path.exists(path):
        frameCount, grid = inputText(path)
        addStructure(0, 0, grid, loaf)
        addStructure (6, 6, grid, blinkerA)
    else:
        width = int(input("Universe Width: ") or "42")
        height = int(input("Universe Height: ") or "42")
        frameCount = int(input("Desired Iterations: ") or "200")
        # populate grid with random on/off - more off than on
        grid = randomGrid(width, height)
        # Uncomment lines to see the "glider" demo
        grid = np.zeros(width*height).reshape(width, height)
        addStructure(0, 0, grid, beaconA)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, ),
                                  frames = frameCount,
                                  interval=updateInterval,
                                  save_count=50)
    ani.save('test.mp4', writer = 'ffmpeg', fps = 12)
    #plt.show()

# call main
if __name__ == '__main__':
    main()