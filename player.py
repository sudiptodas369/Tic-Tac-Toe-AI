import math
import random


class Player():
    def __init__(self, letter):
        # Initialize a player with a specific letter ('X' or 'O')
        self.letter = letter

    def get_move(self, game):
        # This is an abstract method for getting a move. Subclasses will implement it.
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # Get a move from a human player through user input
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # Get a random move from a computer player
        square = random.choice(game.available_moves())
        return square


class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # Get the best move using the minimax algorithm for a smart computer player
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # The player trying to maximize the score (yourself)
        other_player = 'O' if player == 'X' else 'X'  # The opponent player

        # Check if the previous move resulted in a win for the other player
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}  # It's a tie if there are no empty squares left

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Initialize for maximizing player
        else:
            best = {'position': None, 'score': math.inf}  # Initialize for minimizing player
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # Recursively simulate a game after making that move

            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # Represents the move for the optimal next move

            if player == max_player:  # If it's the maximizing player's turn (X)
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:  # If it's the minimizing player's turn (O)
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

