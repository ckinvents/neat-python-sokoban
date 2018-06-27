## 
#  @file evolve_player_parallel.py
#  @brief Module for evolving NEAT Sokoban player.
#  @author Connor Ennis
#  @version 12-27-17
#

import os
import neat
import visualize
import sokoban
from time import time
test_maps = sokoban.map_getter("test_maps")


def main(config_file):
    # Get initial time.
    start_time = time()
    # Load configuration for NEAT-Python.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create population, core of NEAT algorithm.
    pop = neat.Population(config)

    # Create stdout reporter to print progress, currently not implemented.
    pop.add_reporter(neat.StdOutReporter(False))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    
    # Run for unlimited generations max.
    para_eval = neat.ParallelEvaluator(4, play_game)
    winner = pop.run(para_eval.evaluate, 1000)

    # Display winning genome.
    print "\nBest Genome: " + str(winner)
    print "Running Time (in secs.): " + str(time() - start_time)

    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)


def play_game(genome, conf):
    net = neat.nn.FeedForwardNetwork.create(genome, conf)
    player = sokoban.Player(net, "genome" + str(genome.key))
    fitness = 0
    for m in range(len(test_maps[0])):
        game = sokoban.Game(test_maps[0][m], test_maps[1][m], True)
        fitness += game.play(player) * 0.25
    # print "Genome #" + str(genome.key) + " played with fitness " + str(fitness)
    return fitness


if __name__ == "__main__":
    # Path to config, for easy adjustment.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_new")
    main(config_path)

