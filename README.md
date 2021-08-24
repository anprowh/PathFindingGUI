# PathFindingGUI

This program is demonstration of how different pathfinding algorithms work

### Installing and running

To use window version `python main.py`. You can use args `simple`, `twosides`, `astar` to choose algorithm. Like "python main.py astar"

To use web version first run API using `python WebAPI.py`. 

Then run React server by first installing node modules `npm install` then running server `npm start`

If you can't run windowed version or API - try installing python and/or modules from `requirements.txt`

If you can't run web interface - try installing Node.js

### Interface Usage

Use number on your keyboard and backspace to edit "fill value"

Use mouse button to put "fill value" weights in cells.

Use key 'space' to toggle work of the algorithm.

Use key 'r' to reset progress of the algorithm.

Use key 's' to save current environment to ./saved_envs/\*number*.txt file. Where number is the number written in the bottom of the window.

Use key 'l' to load the environment from corresponding to number file.

Use arrow keys (right and left) to speed up / slow down work of the algorithm.
