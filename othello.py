import numpy as np
import time

class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3], self.board[4, 4] = 1, 1
        self.board[3, 4], self.board[4, 3] = -1, -1
        self.current_player = 1  # 1 for black, -1 for white
        self.human_player = None
        self.ai_player = None
        self.big_number = np.inf
        
    def print_board(self):
        symbols = {1: 'B', -1: 'W', 0: '.'}
        print("\n" + "  " + " ".join(str(i) for i in range(8)))  # Column numbers
        for i, row in enumerate(self.board):
            print(str(i) + " " + ' '.join(symbols[cell] for cell in row))
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
        flipped_pieces = []  # Store flipped pieces for undo
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
                        flipped_pieces.append((fr, fc))
                    break
                else:
                    break
                r += dr
                c += dc
        
        if not flipped_pieces:
            self.board[row, col] = 0
            return []
        
        self.current_player *= -1
        return flipped_pieces
    
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
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or not self.has_valid_moves():
            return self.evaluate_board()

        valid_moves = self.get_valid_moves()
    
        if maximizing_player:
            max_eval = -self.big_number
            for move in valid_moves:
                row, col = move
                flipped_pieces = self.place_piece(row, col)  
                if flipped_pieces:  
                    eval = self.minimax(depth - 1, alpha, beta, False)
                    self.undo_move(row, col, flipped_pieces)  
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = self.big_number
            for move in valid_moves:
                row, col = move
                flipped_pieces = self.place_piece(row, col)  
                if flipped_pieces:  
                    eval = self.minimax(depth - 1, alpha, beta, True)
                    self.undo_move(row, col, flipped_pieces)  
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval
        
  #  def evaluate_board(self):
   #     black_score, white_score = self.get_score()
    #    return black_score - white_score

    def evaluate_board(self):
        black_score, white_score = self.get_score()

        # Position weights for strategic play
        corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        adjacent_corners = [(0, 1), (1, 0), (1, 1), (0, 6), (1, 6), (1, 7),
                             (6, 0), (6, 1), (7, 1), (6, 6), (6, 7), (7, 6)]
    
        edge_positions = [(0, i) for i in range(8)] + [(7, i) for i in range(8)] + \
                         [(i, 0) for i in range(8)] + [(i, 7) for i in range(8)]

        # Assign scores based on stability
        corner_value = 100    # Very high priority
        adjacent_corner_value = -25  # Dangerous positions
        edge_value = 10  # Stable edges are good

        # Calculate weighted position scores
        corner_score = sum(self.board[r, c] * corner_value for r, c in corner_positions)
        adjacent_corner_score = sum(self.board[r, c] * adjacent_corner_value for r, c in adjacent_corners)
        edge_score = sum(self.board[r, c] * edge_value for r, c in edge_positions)

        # Calculate the evaluation score, adjusting based on the weights
        return (black_score - white_score) + corner_score + edge_score + adjacent_corner_score 
            

    
    def undo_move(self, row, col, flipped_pieces):
        self.board[row, col] = 0  # Remove placed piece
        for r, c in flipped_pieces:
            self.board[r, c] *= -1  # Flip pieces back
        self.current_player *= -1  # Switch turn back

    
                    
    def ai_move(self, depth):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None
        
        best_move = None
        best_value = -self.big_number
        start_time = time.time()
        
        for move in valid_moves:
            if time.time() - start_time >= 5:
                print("Time limit reached! Making the best move found so far.")
                break
            
            row, col = move
            flipped_pieces = self.place_piece(row, col) 
            if flipped_pieces:
                move_value = self.minimax(depth, -self.big_number, self.big_number, False)
                self.undo_move(row, col, flipped_pieces)  
            
                if move_value > best_value:
                    best_value = move_value
                    best_move = move
        return best_move
    
    def choose_player_color(self):
        while True:
            choice = input("Do you want to play as Black (B) or White (W)? ").strip().upper()
            if choice == "B":
                self.human_player = 1
                self.ai_player = -1
                break
            elif choice == "W":
                self.human_player = -1
                self.ai_player = 1
                break
            else:
                print("Invalid choice. Please enter 'B' for Black or 'W' for White.")       
    
    def play_game(self):
        self.choose_player_color()  

        while self.has_valid_moves():
            self.print_board()
            valid_moves = self.get_valid_moves()
            black_score, white_score = self.get_score()
            print(f"Current player: {'Black' if self.current_player == 1 else 'White'}")
            print(f"Score - Black: {black_score}, White: {white_score}")
            
            if self.current_player == self.human_player:
                valid_moves = self.get_valid_moves()
                print(f"Available moves ({len(valid_moves)}): {valid_moves}")

                while True:
                    try:
                        user_input = input("Enter row and column (0-7) separated by space: ")
                        row, col = map(int, user_input.split())
                        if row <= 7 and col <= 7:
                            self.place_piece(row, col)
                            break
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        print("Invalid input. Please enter two numbers between 0 and 7, separated by a space.")
            else:
                print(f"Available moves ({len(valid_moves)}): {valid_moves}")
                move = self.ai_move(3)
                if move:
                    row, col = move
                    print(f"AI plays: {row} {col}")
                    self.place_piece(row, col)
                else:
                    print("AI has no valid moves, skipping turn.")
        
        self.print_board()
        print(f"Score - Black: {black_score}, White: {white_score}")
        print(self.get_winner())

if __name__ == "__main__":
    game = Othello()
    game.play_game()