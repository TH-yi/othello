from board import Board
from player import Player, HumanPlayer, AIPlayer
import sys
import copy
import threading
from chessboard_recognizer import main as recognize_chessboard
# 游戏
class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None
        self.history = []
        self.recognized_board = None

    def recognize_chessboard_threaded(self):
        done_event = threading.Event()

        def run_recognizer():
            self.recognized_board = recognize_chessboard()
            done_event.set()

        recognizer_thread = threading.Thread(target=run_recognizer)
        recognizer_thread.start()

        done_event.wait()

    # 生成两个玩家
    def make_two_players(self, p=None, level_ix=None, level_iz=None, custom_diff_x=None, custom_diff_o=None):

        '''ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n:")
        p1, p2 = [int(p) for p in ps.split(' ')]'''
        if p == None:
            p = input(
            "Please select a game mode:\n\t0.Player 1 human X VS Player 2  AI   O\n\t1.Player 1  AI   X VS Player 2 "
            "human O\n\t2.Player 1  AI   X VS Player 2  AI   O\n\t3.Player 1 human X VS Player 2 human O\n\t4.Recognize board pic (X first)\n\t5.Recognize board pic (O first)\n")
        try:
            p = int(p)

            if p == 1 or p == 2 or p == 0:  # 至少有一个AI玩家

                if p == 0:
                    level_ix = int(
                        input("Please select the level of AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_ix == 6:  # If user chose customized difficulty
                        if custom_diff_x == None:
                            custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
                        else:
                            custom_difficulty = custom_diff_x
                        if 1 <= custom_difficulty <= 10:
                            custom_iterations = custom_difficulty * 1000
                        else:
                            print("Invalid difficulty. Setting difficulty to 1.")
                            custom_iterations = 1000  # Default value for difficulty 1

                        player1 = HumanPlayer('X')
                        player2 = AIPlayer('O', level_ix)
                        player2.set_custom_iterations(custom_iterations)  # Set custom iterations for the AI player
                    else:
                        player1 = HumanPlayer('X')
                        player2 = AIPlayer('O', level_ix)
                elif p == 1:
                    if level_ix is None:
                        level_ix = int(
                        input("Please select the level of AI player with X.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_ix == 6:  # If user chose customized difficulty
                        if custom_diff_x == None:
                            custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
                        else:
                            custom_difficulty = custom_diff_x
                        if 1 <= custom_difficulty <= 10:
                            custom_iterations = custom_difficulty * 1000
                        else:
                            print("Invalid difficulty. Setting difficulty to 1.")
                            custom_iterations = 1000  # Default value for difficulty 1

                        player2 = HumanPlayer('X')
                        player1 = AIPlayer('O', level_ix)
                        player1.set_custom_iterations(custom_iterations)  # Set custom iterations for the AI player
                    else:

                        player1 = AIPlayer('X', level_ix)
                        player2 = HumanPlayer('O')
                else:
                    if level_ix is None:
                        level_ix = int(
                        input(
                            "Please select the level of AI player with X.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_ix == 6:  # If user chose customized difficulty
                        if custom_diff_x == None:
                            custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
                        else:
                            custom_difficulty = custom_diff_x
                        if 1 <= custom_difficulty <= 10:
                            custom_iterations = custom_difficulty * 1000
                        else:
                            print("Invalid difficulty. Setting difficulty to 1.")
                            custom_iterations = 1000  # Default value for difficulty 1

                        player1 = AIPlayer('X', level_ix)
                        player1.set_custom_iterations(custom_iterations)  # Set custom iterations for the AI player
                    else:
                        player1 = AIPlayer('X', level_ix)
                    if level_iz is None:
                        level_iz = int(
                        input("Please select the level of another AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_iz == 6:  # If user chose customized difficulty
                        if custom_diff_o == None:
                            custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
                        else:
                            custom_difficulty = custom_diff_o
                        if 1 <= custom_difficulty <= 10:
                            custom_iterations = custom_difficulty * 1000
                        else:
                            print("Invalid difficulty. Setting difficulty to 1.")
                            custom_iterations = 1000  # Default value for difficulty 1
                        player2 = AIPlayer('O', level_iz)
                        player2.set_custom_iterations(custom_iterations)  # Set custom iterations for the AI player
                    else:
                        player2 = AIPlayer('O', level_iz)
            elif p == 3 :
                player1, player2 = HumanPlayer('X'), HumanPlayer('O')  # 先手执X，后手执O
            elif p == 4 :
                self.recognize_chessboard_threaded()
                # 从类属性中获取识别的棋盘
                recognized_board = self.recognized_board
                self.board.init_with_recognized_result(recognized_board)
                player1 = HumanPlayer('X')  # 先手执X，后手执O
                player2 = HumanPlayer('O')
            elif p == 5 :
                self.recognize_chessboard_threaded()
                # 从类属性中获取识别的棋盘
                recognized_board = self.recognized_board
                self.board.init_with_recognized_result(recognized_board)
                player1 = HumanPlayer('O')
                player2 = HumanPlayer('X')
            else:
                print('Wrong input! Game start with mode 1')
                if level_ix is None:
                    level_ix = int(
                    input("Please select the level of AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                player1 = HumanPlayer('X')
                player2 = AIPlayer('O', level_ix)
        except(TypeError, ValueError):
            print('Wrong input! Game start with mode 0')
            if level_ix is None:
                level_ix = int(
                input("Please select the level of AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=3)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
            if level_ix == 6:  # If user chose customized difficulty
                if custom_diff_x == None:
                    custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
                else:
                    custom_difficulty = custom_diff_x
                if 1 <= custom_difficulty <= 10:
                    custom_iterations = custom_difficulty * 1000
                else:
                    print("Invalid difficulty. Setting difficulty to 1.")
                    custom_iterations = 1000  # Default value for difficulty 1

                player1 = HumanPlayer('X')
                player2 = AIPlayer('O', level_ix)
                player2.set_custom_iterations(custom_iterations)  # Set custom iterations for the AI player
            else:
                player1 = HumanPlayer('X')
                player2 = AIPlayer('O', level_ix)

        return player1, player2

    # 切换玩家（游戏过程中）
    def switch_player(self, player1, player2):
        if self.current_player is None:
            return player1
        else:
            return [player1, player2][self.current_player == player1]

    # 打印赢家
    def print_winner(self, winner):  # winner in [0,1,2]
        print(['Winner is player1 with X', 'Winner is player2 with O', 'Draw'][winner])

    def generate_moves_by_history(self):
        def number_to_letter(number):
            return chr(ord('A') + number)

        if not self.history:
            return "History is empty or does not exist."

        converted_history = []
        for move in self.history:
            # Check if the move is a tuple and has two elements
            if isinstance(move, tuple) and len(move) == 3:
                try:
                    letter = number_to_letter(move[1][1]).upper()
                    number = move[1][0] + 1
                    converted_move = f"{letter}{number}"
                    converted_history.append(converted_move)
                except (IndexError, TypeError):
                    # If there's an error reading the second element, skip this move
                    continue
            else:
                # Skip invalid moves
                continue
        result = ' '.join(converted_history)
        print(result)
        return ' '.join(converted_history)
    # 运行游戏
    def run(self):
        # 生成两个玩家
        player1, player2 = self.make_two_players()

        # 游戏开始
        print('\nGame start!\n')
        self.board.print_b()  # 显示棋盘

        while True:
            self.current_player = self.switch_player(player1, player2)  # 切换当前玩家

            action = self.current_player.think(self.board)  # 当前玩家对棋盘进行思考后，得到招法

            if action == 'regret':
                if not self.history or (len(self.history) == 1 and self.history[0][3] == 'AIPlayer'):
                    print("No moves to regret!")
                    self.current_player = self.switch_player(player1, player2)
                    continue

                else:
                    last_state, last_action, last_player = self.history[-1]
                    self.history.pop()
                    self.board = last_state
                    #self.current_player.unmove(self.board, last_action, flipped)
                    if isinstance(player1, AIPlayer) or isinstance(player2, AIPlayer):

                        last_state, last_action,last_player = self.history[-1]
                        self.history.pop()
                        self.board = last_state
                        #self.current_player.unmove(self.board, last_action, flipped)
                        self.current_player = self.switch_player(player1, player2)

                    self.board.print_b()

                    print("Regret!")
                    continue

            elif action == 'help':
                action = AIPlayer(self.current_player.color, 3).think(self.board)
                #self.current_player = AIPlayer(player1.color, 3)
            elif action == 'solve':
                player1 = AIPlayer(player1.color, 3)
                player2 = AIPlayer(player2.color, 3)
                self.current_player = self.switch_player(player1, player2)
                action = self.current_player.think(self.board)

            elif action == 'switch_solve':
                player1 = AIPlayer(player1.color, 3)
                player2 = AIPlayer(player2.color, 3)
                self.current_player = self.switch_player(player1, player2)
                self.current_player = self.switch_player(player1, player2)
                action = self.current_player.think(self.board)

            elif action == 'switch':
                continue

            if action is not None:

                #self.history.append((copy.deepcopy(self.board), action, flipped, type(self.current_player).__name__))
                self.history.append((copy.deepcopy(self.board), action, type(self.current_player).__name__))
                flipped = self.current_player.move(self.board, action)
                self.current_player.move(self.board, action)  # 当前玩家执行招法，改变棋盘
                self.board.skip_clear()

            if action is None:
                self.board.skip_increase()
                print('Skipped!')

            self.board.print_b()  # 显示当前棋盘

            if self.board.terminate():  # 根据当前棋盘，判断棋局是否终止
                winner = self.board.get_winner()  # 得到赢家 0,1,2
                self.print_winner(winner)
                print('Game over!\n')
                break


        moves = self.generate_moves_by_history()
        print('history:', moves)
        c = input("Press Enter to exit.")
        sys.exit(0)


if __name__ == '__main__':

    Game().run()
