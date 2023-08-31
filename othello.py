from board import Board
from player import Player, HumanPlayer, AIPlayer
import sys
import copy
import threading



# 游戏
class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None
        self.history = []

    # 生成两个玩家
    def make_two_players(self, p = None):

        '''ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n:")
        p1, p2 = [int(p) for p in ps.split(' ')]'''
        if p == None:
            p = input(
            "Please select a game mode:\n\t0.Player 1 human X VS Player 2  AI   O\n\t1.Player 1  AI   X VS Player 2 "
            "human O\n\t2.Player 1  AI   X VS Player 2  AI   O\n\t3.Player 1 human X VS Player 2 human O\n")
        try:
            p = int(p)

            if p == 1 or p == 2 or p == 0:  # 至少有一个AI玩家

                if p == 0:
                    level_ix = int(
                        input("Please select the level of AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_ix == 6:  # If user chose customized difficulty
                        custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
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
                    level_ix = int(
                        input("Please select the level of AI player with X.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_ix == 6:  # If user chose customized difficulty
                        custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
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
                    level_ix = int(
                        input(
                            "Please select the level of AI player with X.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_ix == 6:  # If user chose customized difficulty
                        custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
                        if 1 <= custom_difficulty <= 10:
                            custom_iterations = custom_difficulty * 1000
                        else:
                            print("Invalid difficulty. Setting difficulty to 1.")
                            custom_iterations = 1000  # Default value for difficulty 1

                        player1 = AIPlayer('X', level_ix)
                        player1.set_custom_iterations(custom_iterations)  # Set custom iterations for the AI player
                    else:
                        player1 = AIPlayer('X', level_ix)
                    level_iz = int(
                        input("Please select the level of another AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                    if level_iz == 6:  # If user chose customized difficulty
                        custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
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
            else:
                print('Wrong input! Game start with mode 1')
                level_ix = int(
                    input("Please select the level of AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=2)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
                player1 = HumanPlayer('X')
                player2 = AIPlayer('O', level_ix)
        except(TypeError, ValueError):
            print('Wrong input! Game start with mode 0')
            level_ix = int(
                input("Please select the level of AI player with O.\n\t0: Beginner (Greedy algorithm, depth=1)\n\t1: Basic (Greedy algorithm with weights map, depth=1)\n\t2: Intermediate (Minimax Algorithm, depth=3)\n\t3: "
                              "Advanced (Minimax Algorithm with α-β Pruning, depth=5)\n\t4: Master (Minimax Algorithm with Pre-Search α-β Pruning, depth=7)\n\t5: Crazy (Monte Carlo Algorithm, iterations=3000 (level 3))\n\t6: Customized (Monte Carlo Algorithm with customized iterations)\n"))
            if level_ix == 6:  # If user chose customized difficulty
                custom_difficulty = int(input("Please select the custom difficulty (1-10): "))
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
                if self.history:
                    last_state, last_action, flipped = self.history.pop()  # 注意这里
                    self.board = last_state
                    self.current_player.unmove(self.board, last_action, flipped)
                    last_state, last_action, flipped = self.history.pop()  # 注意这里
                    self.board = last_state
                    self.current_player.unmove(self.board, last_action, flipped)
                    self.board.print_b()
                    self.current_player = self.switch_player(player1, player2)
                    print("Regret!")
                    continue
                else:
                    print("No moves to regret!")
                    self.current_player = self.switch_player(player1, player2)
                    continue

            if action is not None:
                flipped = self.current_player.move(self.board, action)
                self.history.append((copy.deepcopy(self.board), action, flipped))
                self.current_player.move(self.board, action)  # 当前玩家执行招法，改变棋盘
                self.board.skip_clear()

            if action is None:
                self.board.skip_increase()
                print('Skipped!')

            self.board.print_b()  # 显示当前棋盘

            if self.board.terminate():  # 根据当前棋盘，判断棋局是否终止
                winner = self.board.get_winner()  # 得到赢家 0,1,2
                break

        self.print_winner(winner)
        print('Game over!\n')
        c = input("Press Enter to exit.")
        sys.exit(0)


if __name__ == '__main__':

    Game().run()
