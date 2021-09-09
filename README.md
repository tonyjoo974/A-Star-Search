# Maze Search (BFS vs A-star)
<img src="https://github.com/tonyjoo974/A-Star-Search/blob/main/maze.jpg" width="50%"></img>

## Goal:
Build a general-purpose search algorithms and apply them to solving puzzles. Specifically, I implemented path finding algorithm including BFS and A* for Pacman Game. 

## Requirements:
```
python3
pygame
```
## Running:
The main file to run the mp is mp1.py:

```
usage: mp1.py [-h] [--method {bfs,astar,astar_corner,astar_multi,fast}] [--scale SCALE]
              [--fps FPS] [--human] [--save SAVE]
              filename
```

Examples of how to run MP1:
```
python3 mp1.py bigMaze.txt --method bfs
```
```
python3 mp1.py tinySearch.txt --scale 30 --fps 10 --human
```

For help run:
```
python3 mp1.py -h
```
Help Output:
```
CS440 MP1 Search

positional arguments:
  filename              path to maze file [REQUIRED]

optional arguments:
  -h, --help            show this help message and exit
  --method {bfs,astar,astar_corner,astar_multi,fast}
                        search method - default bfs
  --scale SCALE         scale - default: 20
  --fps FPS             fps for the display - default 30
  --human               flag for human playable - default False
  --save SAVE           save output to image file - default not saved
```
