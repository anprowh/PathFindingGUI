# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Algorithms.SimplePF import SimplePF
from SearchEnvironment import SearchEnvironment
from GUI.SimpleGUI import SimpleGUI



def run():
    environment = SearchEnvironment(21,20,3,16,15,16)
    algorithm = SimplePF(environment)
    GUI = SimpleGUI(algorithm)
    GUI.run()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
