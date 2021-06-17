# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Algorithms.SimplePF import SimplePF
from Algorithms.TwoSidesPF import TwoSidesPF
from Algorithms.AStar import AStar
from SearchEnvironment import SearchEnvironment
from GUI.SimpleGUI import SimpleGUI
import sys


def run():
    environment = SearchEnvironment(21, 20, 3, 16, 15, 5)
    arg_to_alg_dict = {'simple':SimplePF,'twosides':TwoSidesPF,'astar':AStar}
    try:
        algorithm = arg_to_alg_dict[sys.argv[1]](environment)
    except Exception:
        algorithm = SimplePF(environment)
    GUI = SimpleGUI(algorithm)
    GUI.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
