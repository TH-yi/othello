from ai import AI


# 玩家
class Player(object):
    def __init__(self, color):
        self.color = color

    # 思考
    def think(self, board):
        pass

    # 落子
    def move(self, board, action):
        flipped_pos = board._move(action, self.color)
        return flipped_pos

    # 悔子,用于minimax算法复制棋盘推理时调用
    def unmove(self, board, action, flipped_pos):
        board._unmove(action, flipped_pos, self.color)


# 人类玩家
class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def think(self, board):
        while True:
            action = input(
                "Turn to '{}'. \nPlease input a point(such as 'D3'), input 'r' to regret, input 'h' to help, input 's' to let AI solve the endgame: ".format(self.color))
            if action.lower() == 'r' or action.lower() == 'regret':
                return 'regret'
            elif action.lower() == 'h' or action.lower() == 'help':
                return 'help'
            elif action.lower() == 's' or action.lower() == 'solve':
                return 'solve'
            elif action.lower() == 'ss' or action.lower() == 'ssolve':
                return 'switch_solve'
            elif action.lower() == 'sw' or action.lower() == 'switch':
                return 'switch'


            if len(action) < 2:  # Check to make sure action has at least two characters before extracting
                print("Invalid action command. Please try again.")
                continue

            r, c = action[1], action[0].upper()

            # Legality check 1
            if r not in '12345678' or c not in 'ABCDEFGH':
                print("Invalid action. Please enter a valid point between A1 and H8.")
                continue

            x, y = '12345678'.index(r), 'ABCDEFGH'.index(c)

            # Legality check 2
            if (x, y) not in list(board.get_legal_actions(self.color)):
                print("Invalid action. The chosen point is not a legal move.")
                continue

            return x, y


# 电脑玩家（多重继承）
class AIPlayer(Player, AI):

    def __init__(self, color, level_ix=0):
        super().__init__(color)  # init Player
        super(Player, self).__init__(level_ix)  # init AI

    def think(self, board):
        print("Turn to '{}'. \nPlease wait a moment. AI is thinking...".format(self.color))
        uncolor = ['X', 'O'][self.color == 'X']
        opfor = AIPlayer(uncolor)  # 假想敌，陪练

        action = self.brain(board, opfor, 2)
        return action


