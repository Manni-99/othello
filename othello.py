import numpy as np

class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3], self.board[4, 4] = 1, 1
        self.board[3, 4], self.board[4, 3] = -1, -1
        self.current_player = 1  # 1 for black, -1 for white
    
    def print_board(self):
        symbols = {1: 'B', -1: 'W', 0: '.'}
        for row in self.board:
            print(' '.join(symbols[cell] for cell in row))
        print()
    
    def is_valid_move(self, row, col):
        if self.board[row, col] != 0:
            return False
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            has_opponent = False
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r, c] == -self.current_player:
                    has_opponent = True
                elif self.board[r, c] == self.current_player:
                    if has_opponent:
                        return True
                    break
                else:
                    break
                r += dr
                c += dc
        return False
    
    def get_valid_moves(self):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def place_piece(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row, col] = self.current_player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_positions = []
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r, c] == -self.current_player:
                    flip_positions.append((r, c))
                elif self.board[r, c] == self.current_player:
                    for fr, fc in flip_positions:
                        self.board[fr, fc] = self.current_player
                    break
                else:
                    break
                r += dr
                c += dc
        
        self.current_player *= -1
        return True
    
    def has_valid_moves(self):
        return bool(self.get_valid_moves())
    
    def get_score(self):
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == -1)
        return black_count, white_count
    
    def get_winner(self):
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == -1)
        if black_count > white_count:
            return 'Black wins'
        elif white_count > black_count:
            return 'White wins'
        else:
            return 'It\'s a tie!'
    
    def play_game(self):
        while self.has_valid_moves():
            self.print_board()
            valid_moves = self.get_valid_moves()
            black_score, white_score = self.get_score()
            print(f"Current player: {'Black' if self.current_player == 1 else 'White'}")
            print(f"Score - Black: {black_score}, White: {white_score}")
            print(f"Available moves ({len(valid_moves)}): {valid_moves}")
            

            while True:
                try:
                    user_input = input("Enter row and column (0-7) separated by space: ")
                    row, col = map(int, user_input.split())
                    if self.place_piece(row, col):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter two numbers between 0 and 7, separated by a space.")
    
        self.print_board()
        print(self.get_winner())

if __name__ == "__main__":
    game = Othello()
    game.play_game()