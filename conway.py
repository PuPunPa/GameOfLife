"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import os.path

ON = 255
OFF = 0
vals = [ON, OFF]

#Structures
#Stills
block = np.array([[255, 255],
                    [255, 255]])

beehive = np.array([[0, 255, 255, 0],
                    [255, 0, 0, 255],
                    [0, 255, 255, 0]])

loaf = np.array([[0, 255, 255, 0],
                [255, 0, 0, 255],
                [0, 255, 0, 255],
                [0, 0, 255, 0]])

boat = np.array([[255, 255, 0],
                [255, 0, 255],
                [0, 255, 0]])

tub = np.array([[0, 255, 0],
                [255, 0, 255],
                [0, 255, 0]])

#Oscilators
blinkerA = np.array([[255], 
                    [255], 
                    [255]])

blinkerB = np.array([[255, 255, 255]])

toadA = np.array([[0, 0, 255, 0],
           [255, 0, 0, 255],
           [255, 0, 0, 255],
           [0, 255, 0, 0]])

toadB = np.array([[0, 255, 255, 255],
           [255, 255, 255, 0]])

beaconA = np.array([[255, 255, 0, 0],
                    [255, 255, 0, 0],
                    [0, 0, 255, 255],
                    [0, 0, 255, 255]])

beaconB = np.array([[255, 255, 0, 0],
                    [255, 0, 0, 0],
                    [0, 0, 0, 255],
                    [0, 0, 255, 255]])

#Spaceships
gliderA = np.array([[0, 255, 0], 
                    [0, 0, 255], 
                    [255, 255, 255]])

gliderB = np.array([[255, 0, 255], 
                    [0, 255, 255], 
                    [0, 255, 0]])

gliderC = np.array([[0, 0, 255], 
                    [255, 0, 255], 
                    [0,  255, 255]])

gliderD = np.array([[255, 0, 0], 
                    [0, 255, 255], 
                    [255, 255, 0]])

lwShipA = np.array([[255, 0, 0, 255, 0],
                    [0, 0, 0, 0, 255],
                    [255, 0, 0, 0, 255],
                    [0, 255, 255, 255, 255]])

lwShipB = np.array([[0, 0, 255, 255, 0],
                    [255, 255, 0, 255, 255],
                    [255, 255, 255, 255, 0],
                    [0, 255, 255, 0, 0]])

lwShipC = np.array([[0, 255, 255, 255, 255],
                    [255, 0, 0, 0, 255],
                    [0, 0, 0, 0, 255],
                    [255, 0, 0, 255, 0]])

lwShipD = np.array([[0, 255, 255, 0, 0],
                    [255, 255, 255, 255, 0],
                    [255, 255, 0, 255, 255],
                    [0, 0, 255, 255, 0]])
                    
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
    return neighbors - (grid[i, j]/255)

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
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    path = "input.txt"
        
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    frameCount = 0
    
    if os.path.exists(path):
        frameCount, grid = inputText(path)
        addStructure(25, 15, grid, gliderA)
    else:
        width = int(input("Universe Width: ") or "42")
        height = int(input("Universe Height: ") or "42")
        frameCount = int(input("Desired Iterations: ") or "200")
        # populate grid with random on/off - more off than on
        grid = randomGrid(width, height)
        # Uncomment lines to see the "glider" demo
        #grid = np.zeros(N*N).reshape(N, N)

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