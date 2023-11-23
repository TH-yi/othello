import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from board import Board
from player import Player, HumanPlayer, AIPlayer
import sys
from othello import *


class OthelloGUI(tk.Tk):

    def __init__(self, game):
        super().__init__()

        self.game = game
        self.title("Othello")
        self.geometry("330x360")

        self.canvas = tk.Canvas(self, width=320, height=320, bg="green")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_square_click)

        self.info_var = tk.StringVar()
        self.info_var.set("Initializing...")
        self.info_label = ttk.Label(self, textvariable=self.info_var)
        self.info_label.pack(pady=10)

        self.initialize_board_ui()
        self.setup_game()

    def initialize_board_ui(self):
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(i * 40, j * 40, (i + 1) * 40, (j + 1) * 40, fill="green")

    def setup_game(self):
        mode = simpledialog.askstring("Select Mode",
                                      "Please select a game mode:\n\t0.Player 1 human X VS Player 2  AI   O\n\t1.Player 1  AI   X VS Player 2 human O\n\t2.Player 1  AI   X VS Player 2  AI   O\n\t3.Player 1 human X VS Player 2 human O\n")

        if mode:
            mode = int(mode)
            self.player1, self.player2 = self.game.make_two_players(mode)
        else:
            self.player1, self.player2 = self.game.make_two_players(0)
        self.current_player = self.player1
        self.update_info("Game started!")
        self.update_board()

    def on_square_click(self, event):
        if isinstance(self.current_player, HumanPlayer):
            col, row = event.x // 40, event.y // 40
            move = self.current_player.think((row, col))  # Changed this line
            if move:
                self.update_board()
                self.switch_player()
                self.play_turn()

    def update_board(self):
        for i in range(8):
            for j in range(8):
                piece = self.game.board._board[i][j]
                if piece == 'X':
                    self.draw_piece(i, j, 'black')
                elif piece == 'O':
                    self.draw_piece(i, j, 'white')

    def draw_piece(self, x, y, color):
        self.canvas.create_oval(x * 40 + 5, y * 40 + 5, (x + 1) * 40 - 5, (y + 1) * 40 - 5, fill=color)

    def update_info(self, msg):
        self.info_var.set(msg)

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_turn(self):
        if self.game.board.terminate():
            winner = self.game.board.get_winner()
            self.update_info(self.game.print_winner(winner))
            return

        if isinstance(self.current_player, AIPlayer):
            self.update_info("AI is thinking...")
            move = self.current_player.think(self.game.board)
            if move:
                self.current_player.move(self.game.board, move)
                self.update_board()
            self.switch_player()
            self.play_turn()


def main():
    game = Game()
    gui = OthelloGUI(game)
    gui.mainloop()


if __name__ == "__main__":
    main()