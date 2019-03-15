import random
import os

# 游戏类

class Game:
    def __init__(self):
        # 棋盘
        self.board_list = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
        ]
        # 得分
        self.score = 0
        # 空位 存储坐标(行,列)
        self.board_empty = []

    def start(self):
        """
        开始游戏
        :return:
        """
        self.restart()
        while True:
            self.print_board()
            code = input("请输入指令>>>:")
            if code == 'w':
                # 向上
                self.move_up()
            elif code == 's':
                # 向下
                self.move_down()
            elif code == 'a':
                # 向左
                self.move_left()
            elif code == 'd':
                # 向右
                self.move_right()
            elif code == 'r':
                # 重启
                self.restart()
                continue
            elif code == 'q':
                # 退出
                exit("退出")
            else:
                print("你的输入有误,请重新输入")
                continue

            # 判断一下是否赢了
            if self.is_win():
                print("YOU WIN")
                break

            # 判断是否输了
            if self.gameover():
                print("YOU LOSE")
                break

            # 在空白的地方,随机添加2,4
            self.add_piece()

    def print_board(self):
        """
        打印棋盘
        :return:
        """
        print("""SCORE:{}
    +-----+-----+-----+-----+
    |{:^5}|{:^5}|{:^5}|{:^5}|
    +-----+-----+-----+-----+
    |{:^5}|{:^5}|{:^5}|{:^5}|
    +-----+-----+-----+-----+
    |{:^5}|{:^5}|{:^5}|{:^5}|
    +-----+-----+-----+-----+
    |{:^5}|{:^5}|{:^5}|{:^5}|
    +-----+-----+-----+-----+
    w(up),s(down),a(left),d(right)
    r(restart),q(exit)
    """.format(self.score,
               *self.board_list[0],
               *self.board_list[1],
               *self.board_list[2],
               *self.board_list[3],
               ))

    def is_win(self):
        # 判断游戏是否赢了
        # 空位也要找出来
        self.board_empty = []
        for i in range(len(self.board_list)):
            for j in range(len(self.board_list[i])):
                if self.board_list[i][j] == 2048:
                    return True
                if self.board_list[i][j] == '':
                    self.board_empty.append((i, j))

        return False

    def gameover(self):
        # 判断是否输了
        if not self.board_empty:
            # 判断每行每列没有相邻的相等元素
            # 判断每一行
            for i in range(len(self.board_list)):
                for j in range(len(self.board_list[i]) - 1):
                    if self.board_list[i][j] == self.board_list[i][j + 1]:
                        return False
            # 判断每一列
            # 先右转90度
            self.turn_right()
            # 再进行判断
            for i in range(len(self.board_list)):
                for j in range(len(self.board_list[i]) - 1):
                    if self.board_list[i][j] == self.board_list[i][j + 1]:
                        # 左转回去
                        self.turn_left()
                        return False
            return True
        return False

    def add_piece(self):
        # 在空白的地方随机添加2/4
        if self.board_empty:
            # 先随机位置, 并且删除
            p = self.board_empty.pop(random.randrange(len(self.board_empty)))
            # 在随机值
            # random.randrange(左区间, 右区间+1, 步长)
            self.board_list[p[0]][p[1]] = random.randrange(2, 5, 2)

    def restart(self):
        # 初始化棋盘
        self.board_list = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
        ]
        # 得分
        self.score = 0
        # 空位 存储坐标(行,列)
        self.board_empty = []
        # 随机两个位置
        while True:
            t1 = (random.randrange(len(self.board_list)), random.randrange(len(self.board_list[0])))
            t2 = (random.randrange(len(self.board_list)), random.randrange(len(self.board_list[0])))
            if t1 != t2:
                break
        # 随机两个值2/4
        self.board_list[t1[0]][t1[1]] = random.randrange(2, 5, 2)
        self.board_list[t2[0]][t2[1]] = random.randrange(2, 5, 2)

    def move_up(self):
        # 先左转90度
        self.turn_left()
        # 向左操作
        self.move_left()
        # 右转回来
        self.turn_right()

    def move_down(self):
        # 先右转90度
        self.turn_right()
        # 向左操作
        self.move_left()
        # 左转回来
        self.turn_left()

    def move_left(self):
        """
            向左移动
        :return:
        """
        for i in range(len(self.board_list)):
            self.board_list[i] = self.row_left_operator(self.board_list[i])

    def move_right(self):
        # 左转两次
        self.turn_left()
        self.turn_left()
        # 向左操作
        self.move_left()
        # 右转两次
        self.turn_right()
        self.turn_right()

    def row_left_operator(self, row):
        """
            向左把一行列表进行2048操作
        :param row:
        :return:
        """
        # 第一步, 把他们挤到一起, 然后第二步合并同类项, 两两相同的合并, 最后补全
        # l1 = [2, 4, 4, 2]  # => [2, 2, 2] => [4, 2] => [4, 2, '', '']
        # 先挤到一起
        temp = []
        for item in row:
            if item:
                temp.append(item)

        new_row = []
        flag = True
        for i in range(len(temp)):
            if flag:
                # 判断相邻的数是否相等
                if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                    new_row.append(temp[i] * 2)
                    # 改变分数
                    self.score = self.score + temp[i] * 2
                    flag = False
                else:
                    new_row.append(temp[i])
            else:
                flag = True
        # 补齐
        n = len(row)
        for i in range(n - len(new_row)):
            new_row.append('')
        return new_row

    def turn_right(self):
        """
            顺时针旋转90度
        :return:
        """
        # zip()函数对矩阵进行转置
        # item[::-1]对一行进行反转
        self.board_list = [list(x[::-1]) for x in zip(*self.board_list)]

    def turn_left(self):
        """
            逆时针旋转90度
        :return:
        """
        # 逆时针旋转90度等于顺时针旋转270度
        for i in range(3):
            self.turn_right()


if __name__ == '__main__':
    game = Game()
    game.start()