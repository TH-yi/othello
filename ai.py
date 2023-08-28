import sys
import json
import numpy as np
import threading
from board import Board

sys.setrecursionlimit(100000)


class AI(object):
    def __init__(self, level_ix=0):
        # 玩家等级
        self.level = ['beginner', 'basic','intermediate', 'advanced', 'master'][level_ix]
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
        '''super_score1='''
        super_score = int(self.evaluate(board, color)) + 10 * int((self.getstable(board, color))) - 5 * int(
            (self.getmoves(board, uncolor)))

        return super_score



    # AI的大脑
    def brain(self, board, opponent, depth):
        if self.level == 'beginner':  # 入门水平
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                 _, action = self.naive(board)
        elif  self.level == 'basic':  # 初级水平
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.greedy(board)
        elif self.level == 'intermediate':  # 中级水平
            ten_ending = self.is_endgame(board)
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
        elif self.level == 'master': #大师水平
            ten_ending = self.is_endgame(board)
            if ten_ending:
                print("Terminate mode, space left:", ten_ending)
                _, action = self.minimax_terminate(board, opponent, ten_ending, ten_ending)
            else:
                _, action = self.Pre_Search_AlphaBeta(board, opponent, depth + 4)
        # assert action is not None, 'action is None'
        return action

    # 行动力统计,为高级评估函数做准备
    def getmoves(self, board, color):
        moves = len(list(board.get_legal_actions(color)))
        return moves



    def stability(self, board, color, i, j):
        uncolor = ['X', 'O'][color == 'X']
        a = 0  # 四个方向稳定计数器,a=4稳定
        if board[i][j] == color:  # 判定是否为己方棋子
            if i == 0 or i == 7 or j == 0 or j == 7:
                for site in range(4):  # 检测四个方向是否都稳定

                    if site == 0:  # 统计横行方向,以检测该棋子是否"行不可翻"
                        if i == 0 or i == 7:  # 如果横行接边界,横行满足(左右边界棋子不可能被横杀),a+1
                            a += 1

                        else:
                            b = 0
                            for site_a in range(i):  # 检测左侧是否都为己方稳定
                                if board[site_a][j] != color:  # 检测左侧是否都为己方
                                    break
                                if self.stability(board, color, site_a, j) == 0:  # 检测左侧是否都为稳定
                                    break
                                if site_a == i - 1:
                                    a += 1
                                    b += 1
                            if b == 0:  # 如果左侧不为己方稳定,检测右边
                                for site_b in range(i + 1, 8):  # 检测右侧是否都为己方稳定
                                    if board[site_b][j] != color:  # 检测右侧是否都为己方
                                        break
                                    if self.stability(board, color, site_b, j) == 0:  # 检测右侧是否都为稳定
                                        break
                                    if site_b == 7:
                                        a += 1
                                        b += 1
                            if b == 0:  # 如果左右都不全为己方稳定,检测整行是否为敌方稳定
                                for site_c in range(8):
                                    if site_c != i:
                                        if board[site_c][j] != uncolor:  # 检测整行是否都为敌方
                                            break
                                        if self.stability(board, uncolor, site_c, j) == 0:  # 检测整行是否都为敌方稳定
                                            break
                                        if site_c == 7:
                                            a += 1

                    if site == 1:  # 统计竖行方向,以检测该棋子是否"列不可翻"
                        if j == 0 or j == 7:  # 如果竖行接边界,竖列满足(上下边界棋子不可能被竖杀),a+1
                            a += 1

                        else:
                            b = 0
                            for site_d in range(j):  # 检测上侧是否都为己方稳定
                                if board[i][site_d] != color:  # 检测上侧是否都为己方
                                    break
                                if self.stability(board, color, i, site_d) == 0:  # 检测上侧是否都为稳定
                                    break
                                if site_d == j - 1:
                                    a += 1
                                    b += 1
                            if b == 0:  # 如果上侧不为己方稳定,检测下侧
                                for site_e in range(j + 1, 8):  # 检测下侧是否都为己方稳定
                                    if board[i][site_e] != color:  # 检测下侧是否都为己方
                                        break
                                    if self.stability(board, color, i, site_e) == 0:  # 检测下侧是否都为稳定
                                        break
                                    if site_e == 7:
                                        a += 1
                                        b += 1
                            if b == 0:  # 如果上下都不全为己方稳定,检测整列是否为敌方稳定
                                for site_f in range(8):
                                    if site_f != j:
                                        if board[i][site_f] != uncolor:  # 检测 是否都为敌方
                                            break
                                        if self.stability(board, uncolor, i, site_f) == 0:  # 检测整列是否都为敌方稳定
                                            break
                                        if site_f == 7:
                                            a += 1


        if a == 2:
            return 1
        else:
            return 0

    def getstable(self, board, color):
        stable_total = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:  # 遍历棋盘所有己方棋子
                    stable_total += self.stability(board, color, i, j)
        return stable_total

    def is_endgame(self, board):
        #board = board._board
        empty_count = 0
        for row in board:
            for cell in row:
                if cell == '.':
                    empty_count += 1
        if empty_count <= 10:
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
            print('If beginner AI action is', action_b, ', the board value will be', score)
        action_letter = chr(ord('A') + best_action[1])
        action_a = action_letter + str(best_action[0] + 1)
        print('The best action is', action_a, ', the best value is', best_score)

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
            print('If basic AI action is', action_b, ', the board value will be', score)
        action_letter = chr(ord('A') + best_action[1])
        action_a = action_letter + str(best_action[0] + 1)
        print('The best action is', action_a, ', the best value is', best_score)

        return best_score, best_action

    # 极大极小算法，限制深度
    def minimax(self, board, opfor, depth=3):  # 其中 opfor 是假想敌、陪练

        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax(board, self, depth - 1)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            '''if depth>1:
                print (depth)'''
            if depth == 3:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('If intermediate AI action is', action_b, ', the board value will be', score,'at most.')
            if score > best_score:
                best_score = score
                best_action = action
        if depth == 3:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print('The best action is', action_a, ', the best value is', best_score)
        return best_score, best_action

    def minimax_n(self, board, opfor, depth=3):  # 无print版本,服务于预剪枝算法

        color = self.color

        if depth == 0:
            return self.super_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.super_evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax(board, self, depth - 1)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯
            score = -score
            '''if depth>1:
                print (depth)'''

            if score > best_score:
                best_score = score
                best_action = action

        return best_score, best_action


    def minimax_alpha_beta(self, board, opfor, depth=5, alpha=-float('inf'), beta=float('inf')):

        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = -100000
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
            if depth == 5:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('If advanced AI action is', action_b, ', the board value will be', score, 'at most.')

            # Alpha-Beta剪枝
            if best_score >= beta:
                break
            alpha = max(alpha, best_score)

        if depth == 5 and best_action:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print('The best action is', action_a, ', the best value is', best_score)

        return best_score, best_action

    def Pre_Search_AlphaBeta(self, board, opfor, depthm=6, alpha=-float('inf'), beta=float('inf')):
        color = self.color

        if depthm == 0:
            return self.super_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.super_evaluate(board, color), None

        # 预搜索优化，仅在深度大于5时执行
        if depthm > 4:
            Values = []
            for action in action_list:
                flipped_pos = self.move(board, action)
                value, _ = opfor.minimax_n(board, self, 3)  # 假定minimax_n是一个浅层搜索的版本
                self.unmove(board, action, flipped_pos)
                Values.append(value)
            ind = np.argsort(Values)[-8:]  # 仅取最高的8个走法
            action_list = [action_list[i] for i in ind]

        best_score = alpha
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)
            score, _ = opfor.Pre_Search_AlphaBeta(board, self, depthm - 1, -beta, -alpha)
            self.unmove(board, action, flipped_pos)

            score = -score

            if depthm == 6:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print(f'If master AI action is {action_b}, the board value will be {score} at most.')

            if score > best_score:
                best_score = score
                best_action = action
                if best_score >= beta:
                    break
                alpha = max(alpha, best_score)

        if depthm == 6 and best_action:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print(f'The best action is {action_a}, the best value is {best_score}')

        return best_score, best_action

    def minimax_terminate(self, board, opfor, depth, maxdeep):

        color = self.color

        if depth == 0:
            return self.naive_evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.naive_evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax_terminate(board, self, depth - 1, maxdeep)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            '''if depth>1:
                print (depth)'''
            if depth == maxdeep:
                action_letter = chr(ord('A') + action[1])
                action_b = action_letter + str(action[0] + 1)
                print('[terminate]If AI action is', action_b, ', the board absolute value will be', score,'at most.')
            if score > best_score:
                best_score = score
                best_action = action
        if depth == maxdeep:
            action_letter = chr(ord('A') + best_action[1])
            action_a = action_letter + str(best_action[0] + 1)
            print('The best action is', action_a, ', the best value is', best_score)
        return best_score, best_action