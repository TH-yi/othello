class Board(object):
    def __init__(self):
        self.skip = 0
        self.empty = '.'
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]  # 规格：8*8
        self._board[3][4], self._board[4][3] = 'X', 'X'
        self._board[3][3], self._board[4][4] = 'O', 'O'

    # 增加 Board[][] 索引语法
    def __getitem__(self, index):
        return self._board[index]

    def skip_clear(self):  # 正常行棋之后清零skip计数器
        self.skip = 0

    def skip_increase(self):  # 当停步时调用,skip计数器+1
        self.skip += 1

    def skip(self):  # 查询当前skip值
        skip = self.skip()
        return skip

    # 打印棋盘
    def print_b(self):
        board = self._board
        print(' ', ' '.join(list('ABCDEFGH')))
        for i in range(8):
            print(str(i + 1), ' '.join(board[i]))

    # 棋局终止
    def terminate(self):
        list1 = list(self.get_legal_actions('X'))
        list2 = list(self.get_legal_actions('O'))
        skip_now = int(self.skip)
        return [False, True][len(list1) == 0 and len(list2) == 0 or skip_now == 2]

    # 判断赢家
    def get_winner(self):
        s1, s2 = 0, 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 'X':
                    s1 += 1
                if self._board[i][j] == 'O':
                    s2 += 1
        diff = s1 - s2
        sign = '+' if diff > 0 else ''
        print(f'X:O {s1}:{s2} ({sign}{abs(diff)})')
        if s1 > s2:
            return 0  # 黑胜
        elif s1 < s2:
            return 1  # 白胜
        elif s1 == s2:
            return 2  # 平局


    # 落子
    def _move(self, action, color):
        x, y = action
        self._board[x][y] = color

        return self._flip(action, color)

    # 翻子（返回list）
    def _flip(self, action, color):
        flipped_pos = []

        for line in self._get_lines(action):
            for i, p in enumerate(line):
                if self._board[p[0]][p[1]] == self.empty:
                    break
                elif self._board[p[0]][p[1]] == color:
                    flipped_pos.extend(line[:i])
                    break

        for p in flipped_pos:
            self._board[p[0]][p[1]] = color

        return flipped_pos

    # 撤销
    def _unmove(self, action, flipped_pos, color):
        self._board[action[0]][action[1]] = self.empty

        uncolor = ['X', 'O'][color == 'X']
        for p in flipped_pos:
            self._board[p[0]][p[1]] = uncolor

    # 生成8个方向的下标数组，方便后续操作
    def _get_lines(self, action):
        '''说明：刚开始我是用一维棋盘来考虑的，后来改为二维棋盘。偷懒，不想推倒重来，简单地修改了一下'''
        board_coord = [(i, j) for i in range(8) for j in range(8)]  # 棋盘坐标

        r, c = action
        ix = r * 8 + c
        r, c = ix // 8, ix % 8
        left = board_coord[r * 8:ix]  # 要反转
        right = board_coord[ix + 1:(r + 1) * 8]
        top = board_coord[c:ix:8]  # 要反转
        bottom = board_coord[ix + 8:8 * 8:8]

        if r <= c:
            lefttop = board_coord[c - r:ix:9]  # 要反转
            rightbottom = board_coord[ix + 9:(7 - (c - r)) * 8 + 7 + 1:9]
        else:
            lefttop = board_coord[(r - c) * 8:ix:9]  # 要反转
            rightbottom = board_coord[ix + 9:7 * 8 + (7 - (c - r)) + 1:9]

        if r + c <= 7:
            leftbottom = board_coord[ix + 7:(r + c) * 8 + 1:7]
            righttop = board_coord[r + c:ix:7]  # 要反转
        else:
            leftbottom = board_coord[ix + 7:7 * 8 + (r + c) - 6:7]
            righttop = board_coord[((r + c) - 7) * 8 + 7:ix:7]  # 要反转

        # 有四个要反转，方便判断
        left.reverse()
        top.reverse()
        lefttop.reverse()
        righttop.reverse()
        lines = [left, top, lefttop, righttop, right, bottom, leftbottom, rightbottom]
        return lines

    # 检测，位置是否有子可翻
    def _can_fliped(self, action, color):
        flipped_pos = []

        for line in self._get_lines(action):
            for i, p in enumerate(line):
                if self._board[p[0]][p[1]] == self.empty:
                    break
                elif self._board[p[0]][p[1]] == color:
                    flipped_pos.extend(line[:i])
                    break
        return [False, True][len(flipped_pos) > 0]

    # 合法走法
    def get_legal_actions(self, color):
        uncolor = ['X', 'O'][color == 'X']
        uncolor_near_points = []  # 反色邻近的空位

        board = self._board
        for i in range(8):
            for j in range(8):
                if board[i][j] == uncolor:
                    for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1),(-1, -1)]:
                        x, y = i + dx, j + dy
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (
                                x, y) not in uncolor_near_points:
                            uncolor_near_points.append((x, y))
        for p in uncolor_near_points:
            if self._can_fliped(p, color):
                yield p

    def init_with_recognized_result(self, recognized_board):
        for i in range(8):
            for j in range(8):
                if recognized_board[i][j] == 'B':
                    self._board[i][j] = 'X'
                elif recognized_board[i][j] == 'W':
                    self._board[i][j] = 'O'
                else:
                    self._board[i][j] = self.empty



# 测试
if __name__ == '__main__':
    board = Board()
    board.print_b()

    print(list(board.get_legal_actions('X')))

