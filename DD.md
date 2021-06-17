## Functional details
This program runs localy, therefore there is only one type of user.
### Functions:
- Put weights on the grid
  
  You can select which weight to put by pressing numbers on your keyboard. It will change the number written in the bottom of the GUI. Then you can just click or drag cursor over desired cells.
  
  by putting weights on the grid a user creates an environment for the algorithm. If a user starts putting weights when algorithm is in progress - it stops.
- Save the environment
  
  Press 's'. Your environment will be saved to file in folder saved_envs in file \*number*.txt, where \*number* is the number written in the bottom of the GUI.
- Load the environment

  Press 'l'. If file ./saved_envs/\*number*.txt exists, corresponding environment will be loaded.
- Run algorithm

  Press space to toggle mode between running algorithm and drawing weights
- See number of checks and resulting weight

  In the title of the program you can find the number of comparisons made by algorithm and current weight used in algorithm to process cells.
- Change algorithm speed

  By pressing arrow keys (right and left) you can change FPS which increases speed of the algorithm.
- Choose algorithm

  By running file with different arguments you can choose algorithm.
  
### Execution order:
Creating environment object -> Creating algorithm object -> Creating GUI object -> Running GUI object:
Creating main variables used for drawing -> Running main loop:
Handling events (key pressed / mouse button pressed) -> running algorithm step if algorithm not finished -> setting drawing mode if finished -> 
creating matrix of cell types for future coloring -> filling / refilling array of Surfaces with rectangles, texts -> drawing on the main Surface -> setting caption.

### Structure
This project is based on OOP concept. Therefore there are several classes::
- Environment - grid with weights, start point, end point and handy functions to represent this grid as a graph.
- BasePF - abstract class with variables and functions declared or partly realized that all the algorithms have to have for GUI to work.
- \*Other PF Algorithms* - are inherited from BasePF. They have variables needed for them to work and have next_step function realized.
- SimpleGUI - class that uses algorithm and draws GUI
Other structural elements:
- main.py file - main file that you need to run
- saved_envs folder - folder where all the saved envs are stored

### GUI example
![image](https://user-images.githubusercontent.com/48009699/122429231-48037a00-cf9b-11eb-87a3-e891f6181d9f.png)
