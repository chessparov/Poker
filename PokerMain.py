"""

The scope of the following code is to analyze in real time a poker game (valid only fo Texas Hold'em rules).
The classes and methods defined below offer help in calculating the odds and the hands given the user's input.

"""

import PokerGUI as p
import time

if __name__ == "__main__":

    start_time = time.time()

    # Strats the GUI
    p.startWindow()

    print("\nRun time:\t\t--- %s seconds ---" % (round((time.time() - start_time), 5)))