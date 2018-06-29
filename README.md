# neat-python-sokoban

A collection of scripts, config files, and maps used to generate neural networks capable of playing incredibly basic Sokoban puzzles.

Compatible with Python 2.7
You will need to install the neat-python, matplotlib, and graphviz libraries. 

If you have all of the necessary files, run evolve_player_parallel or evolve_player_parallel_reccurent to run. You can also modify the respective config files for each script, and find out more about the available paramenters in NEAT-Python's documentation.
Finally, some of the subdirectories include unique config settings and maps for different trials conducted with the algorithm.
These were used for research, and should function if one desires to tinker with them.

Warning: When this collection of scripts was used for research, they failed to generate any valid solvers for sokoban, and created some unusual behaviors not expected from the algorithm. This could be the product of issues in the NEAT-Python library, but it is currently unknown if that is the case.
