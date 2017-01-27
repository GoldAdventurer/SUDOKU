# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The program looks for twins values (i.e. double-digit numbers that appear twice in a unit). The two digits that compose the number are locked in two boxes. The program then goes over the other boxes in the same unit and remove the two digits from the possible values listed in each box.
    The input is a dictionary and the output the simplified dictionary where the digits that compose the number are removed from the possible values for the peers.  

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The program leverages the eliminate function, the only_choice function, the reduce_puzzle function and the search function. Here is a brief summary of each function's role:
* eliminate: eliminates the number that appear in other boxes from the same unit from the possible values.
* only_choice: whenever a digit appears once in the possible values for boxes of the same unit, the box that contains that unique digit is assigned the digit.
* reduce_puzzle: this function uses successive loops to reduce the sudoku using the eliminate and only_choice functions.
* search: the function chooses a box with the fewest possibilities and attempts to solve multiple sudokus by assigning the possible digits to the box and using a recursive loop.

The two diagonals are added to the unit list.
The input is a string representing the sudoku grid and the output is the solved sudoku in the form of a dictionary.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.