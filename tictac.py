import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")
        
        # Game state
        self.board = [["." for _ in range(3)] for _ in range(3)]
        self.current_player = "O"  # Player 1 starts with O
        self.game_over = False
        self.move_count = 0
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="TIC TAC TOE", 
            font=("Arial", 24, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Player turn indicator
        self.turn_label = tk.Label(
            self.root,
            text="Player 1's Turn (O)",
            font=("Arial", 16),
            fg="#e74c3c",
            bg="#2c3e50"
        )
        self.turn_label.pack(pady=10)
        
        # Game board frame
        board_frame = tk.Frame(self.root, bg="#2c3e50")
        board_frame.pack(pady=20)
        
        # Create 3x3 grid of buttons
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=6,
                    height=3,
                    bg="#34495e",
                    fg="#ecf0f1",
                    activebackground="#3498db",
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.pack(pady=20)
        
        # New game button
        new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Arial", 14),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(
            control_frame,
            text="Quit",
            font=("Arial", 14),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            command=self.root.quit
        )
        quit_btn.pack(side=tk.LEFT, padx=10)
    
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != ".":
            return
        
        # Make the move
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            state="disabled",
            bg="#95a5a6"
        )
        self.move_count += 1
        
        # Check for win
        if self.check_winner():
            self.game_over = True
            winner = "Player 1" if self.current_player == "O" else "Player 2"
            messagebox.showinfo("Game Over", f"{winner} ({self.current_player}) wins!")
            self.highlight_winning_line()
            return
        
        # Check for draw
        if self.move_count >= 9:
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            return
        
        # Switch players
        self.current_player = "X" if self.current_player == "O" else "O"
        player_num = "1" if self.current_player == "O" else "2"
        self.turn_label.config(text=f"Player {player_num}'s Turn ({self.current_player})")
    
    def check_winner(self):
        # Check rows
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] == self.current_player):
                self.winning_line = [(row, 0), (row, 1), (row, 2)]
                return True
        
        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player):
                self.winning_line = [(0, col), (1, col), (2, col)]
                return True
        
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player):
            self.winning_line = [(0, 0), (1, 1), (2, 2)]
            return True
        
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player):
            self.winning_line = [(0, 2), (1, 1), (2, 0)]
            return True
        
        return False
    
    def highlight_winning_line(self):
        if hasattr(self, 'winning_line'):
            for row, col in self.winning_line:
                self.buttons[row][col].config(bg="#27ae60")
    
    def new_game(self):
        # Reset game state
        self.board = [["." for _ in range(3)] for _ in range(3)]
        self.current_player = "O"
        self.game_over = False
        self.move_count = 0
        
        # Reset buttons
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(
                    text="",
                    state="normal",
                    bg="#34495e"
                )
        
        # Reset turn label
        self.turn_label.config(text="Player 1's Turn (O)")
        
        # Remove winning line reference
        if hasattr(self, 'winning_line'):
            delattr(self, 'winning_line')
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()