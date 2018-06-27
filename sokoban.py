## 
#  @file sokoban.py
#  @brief Module for playing Sokoban via a NEAT genome.
#  @author Connor Ennis
#  @version 12-26-17
#

# Class definitions.


class Game:
    """Represents a Sokoban board for a puzzle."""
    INVALID_MAX = 10
    INPUTS_DICT = {0: 0, 1: -1, 2: -0.5, 4: 1, 8: 0.5}

    def __init__(self, board_map, weighted_map, is_silent):
        self.map = board_map
        self.map_weighted = weighted_map
        self.solutions = self.find(4)
        self.is_silent = is_silent

    # Support Methods.

    # Prints if is_silent = False
    def print_silenced(self, output):
        if not self.is_silent:
            print output,

    # Displays map if is_silent = False
    def display_map(self):
        self.print_silenced("Sokoban")
        for y in self.map:
            self.print_silenced("\n\t",)
            for x in y:
                self.print_silenced(str(x) + " ",)
        self.print_silenced("\n")

    # Converts map into a network-friendly series of inputs.
    def convert_map(self):
        inputs = []
        for y in self.map:
            for x in y:
                inputs.append(Game.INPUTS_DICT[x])
        return inputs

    # Finds an item in self's map array, and returns a list of coordinate lists at which it occurs.
    def find(self, item):
        coords = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if item == self.map[y][x]:
                    coords.append([x, y])
        return coords

    # Finds if a player has won by comparing the solutions list to the
    def get_solved(self):
        is_solved = False
        if self.solutions == self.find(2):
            is_solved = True
            self.print_silenced("Solved")
        return is_solved

    # Attempts to apply player move to game. If false is returned, player move invalid.
    def apply_move(self, move):
        could_move = True
        # Get player and crate locations.
        player_coords = self.find(8)[0]
        crate_coords = self.find(2)[0]
        player_on_tile = 0
        crate_on_tile = 0
        # See if either is on a goal.
        if player_coords in self.solutions:
            player_on_tile = 4
        if crate_coords in self.solutions:
            crate_on_tile = 4
        if move == 0:
            player_coords[1] -= 1
            if player_coords == crate_coords:
                crate_coords[1] -= 1
                if self.map[crate_coords[1]][crate_coords[0]] in (0, 4):
                    self.map[crate_coords[1]][crate_coords[0]] = 2
                    self.map[crate_coords[1] + 1][crate_coords[0]] = crate_on_tile
                else:
                    could_move = False
            if self.map[player_coords[1]][player_coords[0]] in (0, 4):
                self.map[player_coords[1]][player_coords[0]] = 8
                self.map[player_coords[1] + 1][player_coords[0]] = player_on_tile
            else:
                could_move = False
        elif move == 1:
            player_coords[0] += 1
            if player_coords == crate_coords:
                crate_coords[0] += 1
                if self.map[crate_coords[1]][crate_coords[0]] in (0, 4):
                    self.map[crate_coords[1]][crate_coords[0]] = 2
                    self.map[crate_coords[1]][crate_coords[0] - 1] = crate_on_tile
                else:
                    could_move = False
            if self.map[player_coords[1]][player_coords[0]] in (0, 4):
                self.map[player_coords[1]][player_coords[0]] = 8
                self.map[player_coords[1]][player_coords[0] - 1] = player_on_tile
            else:
                could_move = False
        elif move == 2:
            player_coords[1] += 1
            if player_coords == crate_coords:
                crate_coords[1] += 1
                if self.map[crate_coords[1]][crate_coords[0]] in (0, 4):
                    self.map[crate_coords[1]][crate_coords[0]] = 2
                    self.map[crate_coords[1] - 1][crate_coords[0]] = crate_on_tile
                else:
                    could_move = False
            if self.map[player_coords[1]][player_coords[0]] in (0, 4):
                self.map[player_coords[1]][player_coords[0]] = 8
                self.map[player_coords[1] - 1][player_coords[0]] = player_on_tile
            else:
                could_move = False
        elif move == 4:
            player_coords[0] -= 1
            if player_coords == crate_coords:
                crate_coords[0] -= 1
                if self.map[crate_coords[1]][crate_coords[0]] in (0, 4):
                    self.map[crate_coords[1]][crate_coords[0]] = 2
                    self.map[crate_coords[1]][crate_coords[0] + 1] = crate_on_tile
                else:
                    could_move = False
            if self.map[player_coords[1]][player_coords[0]] in (0, 4):
                self.map[player_coords[1]][player_coords[0]] = 8
                self.map[player_coords[1]][player_coords[0] + 1] = player_on_tile
            else:
                could_move = False
        return could_move

    # Core Method. (Gameplay)

    # Updates the puzzle for each move made until solved.
    def play(self, player):
        is_solved = False
        invalid_count = 0
        move_count = 0
        score = 1
        # Loop until puzzle solved, increment turn each time.
        while not is_solved and invalid_count <= Game.INVALID_MAX and move_count <= Game.INVALID_MAX:
            move_valid = False
            while not move_valid and invalid_count <= Game.INVALID_MAX:
                self.display_map()
                move = player.get_move(self)
                move_valid = self.apply_move(move)
                if not move_valid:
                    invalid_count += 1
                    score -= 0.01
                    self.print_silenced("Invalid move.")
            is_solved = self.get_solved()
            move_count += 1
        if is_solved:
            score = 1
        else:  # Timeout, score according to distance from solution. Should encourage closer solutions.
            crate_coord = self.find(2)[0]
            score = 1 - self.map_weighted[crate_coord[1]][crate_coord[0]]
        return score


class Player:
    """Represents a Sokoban player for a puzzle."""
    def __init__(self, network, name):
        if network is not None:
            self.network = network
            self.type = "NEAT"
        else:
            self.network = None
            self.type = "Human"
        self.name = name

    # Calculates a player's move from inputs (player or NEAT) and returns a number representing the move.
    # 0 - UP  1 - RIGHT  2 - DOWN  4 - LEFT
    def get_move(self, game):
        ret_move = -1
        if self.type == "NEAT":
            move = self.network.activate(game.convert_map())[0]
            if move >= 0.75:
                ret_move = 4
            elif move >= 0.5:
                ret_move = 2
            elif move >= 0.25:
                ret_move = 1
            else:
                ret_move = 0
        elif self.type == "Human":
            while ret_move == -1:
                move = raw_input("Please enter move from NumPad key: ")
                if move == "8":
                    ret_move = 0
                elif move == "6":
                    ret_move = 1
                elif move == "2":
                    ret_move = 2
                elif move == "4":
                    ret_move = 4
                else:
                    print "Invalid input."
        return ret_move


def map_getter(map_list):
    with open(map_list, 'r') as file_in:
        current = file_in.readline()
        char_maps = []
        weight_maps = []
        while current != '':
            char_map = []
            weight_map = []
            while current != '\n' and current != 'w\n' and current != 'w\r\n':
                map_line = []
                for c in current:
                    if c != '\n' and c != '\r' and c != ' ':
                        map_line.append(int(c))
                current = file_in.readline()
                char_map.append(map_line)
            if current != 'w\n' and current != 'w\r\n':
                break
            if current == 'w\n' or current == 'w\r\n':
                current = file_in.readline()
                float_block = ''
                while current != '\n' and current != '\r\n' and current != '':
                    map_line = []
                    for c in current:
                        if c != '\n' and c != '\r' and c != ' ':
                            float_block += c
                        elif float_block != '':
                            map_line.append(float(float_block))
                            float_block = ''
                    if float_block != '':
                        map_line.append(float(float_block))
                    current = file_in.readline()
                    weight_map.append(map_line)
            char_maps.append(char_map)
            weight_maps.append(weight_map)
            current = file_in.readline()
        return [char_maps, weight_maps]


if __name__ == "__main__":
    test_map = []
    test_file = "test_maps"
    all_maps = map_getter(test_file)
    # test_map = [all_maps[0][0], all_maps[1][0]]
    for m in range(len(all_maps[0])):
        test_game = Game(all_maps[0][m], all_maps[1][m], False)
        test_player = Player(None, "Player 1")
        test_game.play(test_player)
