## Artificial Intelligence - Search

### 8 Puzzle Solver

<div align="center">
<img src="https://github.com/athom031/Artificial_Intelligence/blob/master/8-Puzzle-Solver/demo_img/nodeAnalysis.png" width = "50%"/> 
</div><br/>

## Abstract
A python implementation of a search solution to the 8 puzzle [problem](https://blog.goodaudience.com/solving-8-puzzle-using-a-algorithm-7b509c331288). <br/>

Three methods are used to show the merit of A* search and within that, the importance of a good heuristic.<br/>
Uniform Cost Search only depends on the movement cost to determine the next move.<br/>
A* Search uses the movement cost to determine the next move but adding to that includes a heuristic function to determine the best next step. The A* search used, depends on two different heuristics.<br/>
_Misplaced Tile_ checks how many tiles are where they shouldn't be. <br/>
_Manhattan Distance_ checks how far each tile is from where it should be. <br/>

## Getting Started

This is a python project.<br/>
First install python on to your system. <br/>
[Mac Python 3 Download](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)

### Prerequisites

All modules used are default libraries of python.

### Compile

To run the 8-Puzzle Solver interface:
```
python puzzle.py
```	
The option is given to either use a default puzzle or enter your own.<br/>
Then the option is given to pick which search algorithm to use, to find the path. <br/>

## Reflection

<div align="center">
<img src="https://github.com/athom031/Artificial_Intelligence/blob/master/8-Puzzle-Solver/demo_img/runtime.png" width = "50%"/> 
</div><br/>

We can see building upon the movement cost to predict the next best step, reduces the runtime and space complexity exponentially. The heuristic chosen also matters. I was surprised that the misplaced tile performed better for this example than the Manhattan distance because from theory, the Manhattan distance uses more information about the actual state. But they are very similar and might vary for other examples.