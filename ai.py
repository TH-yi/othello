import sys
import random
import numpy as np
import threading
from board import Board
import copy
from math import sqrt, log


sys.setrecursionlimit(1000000000)

class AI(object):
    def __init__(self, level_ix=0):
        # 玩家等级
        self.level = ['beginner', 'basic','intermediate', 'advanced', 'master', 'crazy', 'customized', 'text'][level_ix]
        # 棋盘位置权重
        self.board_weights = [
            [500, -25, 10, 5, 5, 10, -25, 500],
            [-25, -45, 1, 1, 1, 1, -45, -25],
            [10, 1, 3, 2, 2, 3, 1, 10],
            [5, 1, 2, 1, 1, 2, 1, 5],
            [5, 1, 2, 1, 1, 2, 1, 5],
            [10, 1, 3, 2, 2, 3, 1, 10],
            [-25, -45, 1, 1, 1, 1, -45, -25],
            [500, -25, 10, 5, 5, 10, -25, 500]
        ]
        self.weight = [6, 11, 2, 2, 3]
        self.transposition_table = {}  # 置换表
        self.memo = {} #stable cache

    class TreeNode(object):
        def __init__(self, state, parent=None, action=None):
            self.state = state
            self.parent = parent
            self.action = action
            self.children = []
            self.wins = 0
            self.visits = 0

        def select_child(self):
            """选择UCB1值最高的子节点"""
            s = sorted(self.children, key=lambda c: c.wins / (c.visits + 1e-10) + sqrt(2 * log(self.visits + 1e-10) / (c.visits + 1e-10)))
            return s[-1]

        def add_child(self, node):
            self.children.append(node)

    def set_custom_iterations(self, num):
        self.custom_iterations = num

    # AI的大脑
    def brain(self, board, opponent, depth):
        if self.level == 'beginner':  # 入门水平
            ten_ending = self.is_endgame(board, space = 7)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.naive(board)
        elif self.level == 'basic':  # 初级水平
            ten_ending = self.is_endgame(board, space = 8)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.greedy(board)
        elif self.level == 'intermediate':  # 中级水平
            ten_ending = self.is_endgame(board, space = 9)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.minimax(board, opponent, depth + 1)
        elif self.level == 'advanced':  # 高级水平
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.minimax_alpha_beta(board, opponent, depth + 3)
        elif self.level == 'master':  # 大师水平
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.Pre_Search_AlphaBeta(board, opponent, depth + 5)

        elif self.level == 'crazy':
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                action = self.MCTS(board, 3000)

        elif self.level == 'customized':  # Check for customized level
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                action = self.MCTS(board, self.custom_iterations)  # Use the custom number of iterations

        elif self.level == 'text':  # 大师水平
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.nPre_Search_AlphaBeta(board, opponent, 15)
        # assert action is not None, 'action is None'
        return action

    def MCTS(self, board, iterations):
        root = self.TreeNode(board)
        level_crz = iterations // 1000
        legal_actions = list(root.state.get_legal_actions(self.color))
        # Check for 0 or 1 legal action
        if len(legal_actions) == 0:
            print('For crazy AI level ' + str(level_crz) + ', action is skip!')
            return None
        elif len(legal_actions) == 1:
            action_only = legal_actions[0]
            action_letter = chr(ord('A') + action_only[1])
            action_b = action_letter + str(action_only[0] + 1)
            print('For crazy AI level ' + str(level_crz) + ', the only action is ' + str(action_b))
            return action_only

        for _ in range(iterations):
            node = root
            # Selection
            while len(node.children) == len(list(node.state.get_legal_actions(self.color))) and node.children:
                node = node.select_child()

            # Expansion
            legal_actions = list(node.state.get_legal_actions(self.color))
            for action in legal_actions:
                if action not in [child.action for child in node.children]:
                    new_board = copy.deepcopy(node.state)
                    new_board._move(action, self.color)
                    node.add_child(self.TreeNode(new_board, parent=node, action=action))

            # Simulation
            current_board = copy.deepcopy(node.state)
            current_color = self.color
            while list(current_board.get_legal_actions(current_color)) or list(current_board.get_legal_actions(
                    'X' if current_color == 'O' else 'O')):
                current_actions = list(current_board.get_legal_actions(current_color))
                if not current_actions:
                    current_color = 'X' if current_color == 'O' else 'O'
                    continue
                action = random.choice(current_actions)
                current_board._move(action, current_color)
                current_color = 'X' if current_color == 'O' else 'O'

            # Backpropagation
            result = self.evaluate(current_board, self.color)
            while node:
                node.visits += 1
                if result > 0:  # Modify this to fit your evaluation
                    node.wins += 1
                node = node.parent
        # 这里移动打印代码，只在所有模拟完成后打印一次
        total_score = sum([child.wins / child.visits if child.visits != 0 else 0 for child in root.children])

        weighted_actions = []

        for child in root.children:
            action = child.action
            score = child.wins / child.visits if child.visits != 0 else 0
            weight = score / total_score if total_score != 0 else 0
            weight_squared = (10*weight) ** 4
            weighted_actions.append((action, weight_squared))


        # 重新计算权重，使其和为1
        weight_sum = sum([weight for _, weight in weighted_actions])
        if weight_sum == 0:
            try:
                action_only = sorted(root.children, key=lambda c: c.visits)[-1].action
                action_letter = chr(ord('A') + action_only[1])
                action_b = action_letter + str(action_only[0] + 1)
                print('For crazy AI level ' + str(level_crz) + ', the only action is ' + str(action_b))
                return action_only
            except:
                print('For crazy AI level ' + str(level_crz) + ', action is skip!')
                return None
        else:
            for idx, (action, weight) in enumerate(weighted_actions):
                weighted_actions[idx] = (action, weight / weight_sum)

            weighted_actions.sort(key=lambda x: x[1], reverse=True)
            for action, weight in weighted_actions:
                formatted_weight = "{:.3%}".format(weight)
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('For crazy AI level ' + str(level_crz) + ', action '+ str(action_b) +  ' weight is', formatted_weight)

            best_action, best_weight = weighted_actions[0]
            best_action_letter = chr(ord('A') + best_action[1])
            best_action_str = best_action_letter + str(best_action[0] + 1)
            print('The best action is ' + str(best_action_str)+ ', its weight is', "{:.3%}".format(best_weight))

            return best_action

    # 评估函数（仅根据棋盘位置权重）
    def evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    score += self.board_weights[i][j]

                elif board[i][j] == uncolor:
                    score -= self.board_weights[i][j]

        return score

    def naive_evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    score += 1
                elif board[i][j] == uncolor:
                    score -= 1
        return score

    def super_evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        # 计算前沿子
        frontier = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == 0:
                    continue
                # 检查周围的8个方向
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == 0:
                        frontier -= board[row][col]
                        break

        # 计算奇偶性
        parity = 0
        if self.getmoves(board, color) + self.getmoves(board, uncolor) < 18:
            parity = 1 if (self.getmoves(board, color) + self.getmoves(board, uncolor)) % 2 == 0 else -1

        rv = frontier * self.weight[2] +  parity * self.weight[4]
        super_score = int(rv) + int(self.evaluate(board, color)) + 7 * int((self.getstable(board, color))) - 7 * int((self.getstable(board, uncolor))) + 15* int(
            self.getmoves(board, color))- 15* int(self.getmoves(board, uncolor))

        return super_score

    def nsuper_evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']

        # 计算棋盘上的棋子数量来确定轮数
        round = sum([row.count('X') + row.count('O') for row in board])

        # 计算前沿子
        frontier = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == color:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == uncolor:
                            frontier -= 1
                            break

        # 计算奇偶性
        parity = 0
        total_moves = self.getmoves(board, color) + self.getmoves(board, uncolor)
        if total_moves < 18:
            parity = 1 if total_moves % 2 == 0 else -1

        # 轮数相关的权重
        a1 = (64.0 - round) / 64.0
        a2 = (64.0 - round) / 64.0
        a3 = round / 64.0 * 10
        a4 = 1 / ((round - 32) * (round - 32) + 0.1)

        rv = a1 * frontier * self.weight[2] + a2 * parity * self.weight[4]
        super_score = int(rv) + int(a3 * self.evaluate(board, color)) + 10 * int(a4 * self.getstable(board, color)) + 15 * int(
            self.getmoves(board, color)) - 15 * int(self.getmoves(board, uncolor))

        return super_score
    # 行动力统计,为高级评估函数做准备
    def getmoves(self, board, color):
        moves = len(list(board.get_legal_actions(color)))
        return moves

    def is_stable(self, board, color, i, j):
        if board[i][j] != color:
            return False

        # Check horizontal stability
        left_stable = all(board[x][j] == color for x in range(i))
        right_stable = all(board[x][j] == color for x in range(i + 1, 8))

        # Check vertical stability
        up_stable = all(board[i][y] == color for y in range(j))
        down_stable = all(board[i][y] == color for y in range(j + 1, 8))

        return (left_stable or right_stable) and (up_stable or down_stable)

    def getstable(self, board, color):
        stable_count = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color and self.is_stable(board, color, i, j):
                    stable_count += 1
        return stable_count

    def is_endgame(self, board, space = 10):
        #board = board._board
        empty_count = 0
        for row in board:
            for cell in row:
                if cell == '.':
                    empty_count += 1
        if empty_count <= space:
            return empty_count
        else:
            return False

    def naive(self, board): #幼稚贪婪算法
        color = self.color

        action_list = list(board.get_legal_actions(color))

        if not action_list:
            return self.naive_evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)
            score = self.naive_evaluate(board, color)
            self.unmove(board, action, flipped_pos)  # 回溯

            if score > best_score:
                best_score = score
                best_action = action

            action_letter = chr(ord('A') + action[1])
            action_b = action_letter + str(action[0] + 1)
            print('If beginner AI action is '+ str(action_b) +  ', the board value will be', score)
        action_letter = chr(ord('A') + best_action[1])
        action_a = action_letter + str(best_action[0] + 1)
        print('The best action is '+ str(action_a) +  ', the best value is', best_score)

        return best_score, best_action

    # 贪婪算法（只想一步棋）
    def greedy(self, board):
        color = self.color

        action_list = list(board.get_legal_actions(color))

        if not action_list:
            return self.evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)
            score = self.evaluate(board, color)
            self.unmove(board, action, flipped_pos)  # 回溯

            if score > best_score:
                best_score = score
                best_action = action

            action_letter = chr(ord('A') + action[1])
            action_b = action_letter + str(action[0] + 1)
            print('If basic AI action is '+ str(action_b) +  ', the board value will be', score)
        action_letter = chr(ord('A') + best_action[1])
        action_a = action_letter + str(best_action[0] + 1)
        print('The best action is '+ str(action_a) +  ', the best value is', best_score)

        return best_score, best_action

    # 极大极小算法，限制深度
    def minimax(self, board, opfor, depth=3, skipped=False):  # 其中 opfor 是假想敌、陪练

        color = self.color
        best_score = -100000
        best_action = None

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            if not skipped:
                score, _ = opfor.minimax(board, self, depth, skipped=True)
                score = -score
            else:
                score, _ = opfor.minimax(board, self, 0, skipped=True)
                score = -score

            if score > best_score:
                best_score = score
                best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax(board, self, depth - 1)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            '''if depth>1:
                print (depth)'''
            if depth == 3 and not skipped:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('If intermediate AI action is '+ str(action_b) +  ', the board value will be', score,'.')
            if score > best_score:
                best_score = score
                best_action = action
        if depth == 3 and not skipped:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print('The best action is '+ str(action_a) +  ', the best value is', best_score)
        return best_score, best_action

    def minimax_n(self, board, opfor, depth=2, skipped=False):  # 无print版本,服务于预剪枝算法
        color = self.color

        best_score = -float('inf')  # 修改初始化值
        best_action = None
        if depth == 0:
            return self.super_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            if not skipped:
                score, _ = opfor.minimax_n(board, self, depth, skipped=True)
                score = -score
            else:
                score, _ = opfor.minimax_n(board, self, 0, skipped=True)
                score = -score

            if score > best_score:
                best_score = score
                best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)
            score, _ = opfor.minimax_n(board, self, depth - 1)  # 修改递归调用
            self.unmove(board, action, flipped_pos)
            score = -score

            if score > best_score:
                best_score = score
                best_action = action

        return best_score, best_action


    def minimax_alpha_beta(self, board, opfor, depth=5, alpha=-float('inf'), beta=float('inf'), skipped=False):

        color = self.color

        best_score = -100000
        best_action = None

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            if not skipped:
                score, _ = opfor.minimax_alpha_beta(board, self, depth, -beta, -alpha, skipped=True)
                score = -score
            else:
                score, _ = opfor.minimax_alpha_beta(board, self, 0, -beta, -alpha, skipped=True)
                score = -score

            if score > best_score:
                best_score = score
                best_action = None


        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax_alpha_beta(board, self, depth - 1, -beta, -alpha)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score

            # 更新最佳得分和动作
            if score > best_score:
                best_score = score
                best_action = action

            # 输出对应深度为5的动作和评分
            if depth == 5 and not skipped:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('If advanced AI action is '+ str(action_b) +  ', the board value will be', score, '.')

            # Alpha-Beta剪枝
            if best_score >= beta:
                break
            alpha = max(alpha, best_score)

        if depth == 5 and best_action and not skipped:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print('The best action is '+ str(action_a) +  ', the best value is', best_score)

        return best_score, best_action

    def Pre_Search_AlphaBeta(self, board, opfor, depthm=7, alpha=-float('inf'), beta=float('inf'), skipped=False):
        color = self.color

        best_score = -100000
        best_action = None

        if depthm == 0:
            return self.super_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            if not skipped:
                score, _ = opfor.Pre_Search_AlphaBeta(board, self, depthm, -beta, -alpha, skipped = True)
                score = -score
            else:
                score, _ = opfor.Pre_Search_AlphaBeta(board, self, 0, -beta, -alpha, skipped = True)
                score = -score

            if score > best_score:
                best_score = score
                best_action = None

        # 预搜索优化，仅在深度大于6时执行
        if depthm > 6:
            Values = []
            for action in action_list:
                flipped_pos = self.move(board, action)
                value, _ = opfor.minimax_n(board, self, 2)  # 假定minimax_n是一个浅层搜索的版本
                self.unmove(board, action, flipped_pos)
                Values.append(value)
                # 获取要考虑的走法数量，最多为8，但不超过实际走法数量
            num_actions_to_consider = min(8, len(action_list))

            ind = np.argsort(Values)[-num_actions_to_consider:]  # 仅取最高的num_actions_to_consider个走法
            action_list = [action_list[i] for i in ind]



        if depthm == 7 and len(action_list) ==1 and not skipped:
            best_action = action_list[0]
            best_score = 0
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print(f'Master AI only one action is {action_a}')
            return best_score, best_action
        else:
            for action in action_list:
                flipped_pos = self.move(board, action)
                score, _ = opfor.Pre_Search_AlphaBeta(board, self, depthm - 1, -beta, -alpha)
                self.unmove(board, action, flipped_pos)

                score = -score

                # 更新最佳得分和动作
                if score > best_score:
                    best_score = score
                    best_action = action

                if depthm == 7 and not skipped:
                    action_letter = chr(ord('A') + action[1])
                    action_b = action_letter + str(action[0] + 1)
                    print(f'If master AI action is {action_b}, the board value will be {score}.')

                # Alpha-Beta剪枝
                if best_score >= beta:
                    break
                alpha = max(alpha, best_score)

        if depthm == 7 and best_action and not skipped:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print(f'The best action is {action_a}, the best value is {best_score}')

        return best_score, best_action

    def nPre_Search_AlphaBeta(self, board, opfor, depthm=15, alpha=-float('inf'), beta=float('inf'), skipped=False):
        color = self.color

        best_score = -100000
        best_action = None

        if depthm == 0:
            return self.nsuper_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            if not skipped:
                score, _ = opfor.Pre_Search_AlphaBeta(board, self, depthm, -beta, -alpha, skipped = True)
                score = -score
            else:
                score, _ = opfor.Pre_Search_AlphaBeta(board, self, 0, -beta, -alpha, skipped = True)
                score = -score

            if score > best_score:
                best_score = score
                best_action = None

        # 预搜索优化，仅在深度大于6时执行
        if depthm > 6:
            Values = []
            for action in action_list:
                flipped_pos = self.move(board, action)
                value, _ = opfor.minimax_n(board, self, 2)  # 假定minimax_n是一个浅层搜索的版本
                self.unmove(board, action, flipped_pos)
                Values.append(value)
                # 获取要考虑的走法数量，最多为8，但不超过实际走法数量
            num_actions_to_consider = min(8, len(action_list))

            ind = np.argsort(Values)[-num_actions_to_consider:]  # 仅取最高的num_actions_to_consider个走法
            action_list = [action_list[i] for i in ind]



        if depthm == 15 and len(action_list) ==1 and not skipped:
            best_action = action_list[0]
            best_score = 0
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print(f'Master AI only one action is {action_a}')
            return best_score, best_action
        else:
            for action in action_list:
                flipped_pos = self.move(board, action)
                score, _ = opfor.nPre_Search_AlphaBeta(board, self, depthm - 1, -beta, -alpha)
                self.unmove(board, action, flipped_pos)

                score = -score

                # 更新最佳得分和动作
                if score > best_score:
                    best_score = score
                    best_action = action

                if depthm == 15 and not skipped:
                    action_letter = chr(ord('A') + action[1])
                    action_b = action_letter + str(action[0] + 1)
                    print(f'If master AI action is {action_b}, the board value will be {score}.')

                # Alpha-Beta剪枝
                if best_score >= beta:
                    break
                alpha = max(alpha, best_score)

        if depthm == 15 and best_action and not skipped:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print(f'The best action is {action_a}, the best value is {best_score}')

        return best_score, best_action
    def minimax_terminate(self, board, opfor, depth, maxdeep, skipped = False):

        color = self.color
        best_score = -100000
        best_action = None

        if depth == 0:
            return self.naive_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            if not skipped:
                score, _ = opfor.minimax_terminate(board, self, depth, maxdeep, skipped = True)
                score = -score
            else:
                score, _ = opfor.minimax_terminate(board, self, 0, maxdeep, skipped=True)
                score = -score

            if score > best_score:
                best_score = score
                best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax_terminate(board, self, depth - 1, maxdeep)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            '''if depth>1:
                print (depth)'''
            if depth == maxdeep and not skipped:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('[terminate]If AI action is '+ str(action_b) +  ', the board absolute value will be', score,'.')
            if score > best_score:
                best_score = score
                best_action = action
        if depth == maxdeep and not skipped:
            if not best_action:
                print("No action, skip!")
            else:
                action_letter = chr(ord('A') + best_action[1])
                action_a = action_letter + str(best_action[0] + 1)
                print('[terminate]The best action is '+ str(action_a) +  ', the best value is', best_score)
        return best_score, best_action

