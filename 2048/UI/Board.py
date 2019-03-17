#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random


class Board:

    def __init__(self):
        # 当前矩阵
        self.board_list = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
        ]
        # 空矩阵 存储坐标(行,列)
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

    def addPiece(self):
        """
        在空白的地方随机添加2/4
        :return:
        """
        if self.board_empty:
            # 先随机位置, 并且删除
            p = self.board_empty.pop(random.randrange(len(self.board_empty)))
            # 在随机值
            # random.randrange(左区间, 右区间+1, 步长)
            self.board_list[p[0]][p[1]] = random.randrange(2, 5, 2)

    def moveUp(self, score):
        # 先左转90度
        self.turnLeft()
        # 向左操作
        score = self.moveLeft(score)
        # 右转回来
        self.turnRight()
        return score

    def moveDown(self, score):
        # 先右转90度
        self.turnRight()
        # 向左操作
        score = self.moveLeft(score)
        # 左转回来
        self.turnLeft()
        return score

    def moveLeft(self, score):
        """
        向左移动
        :return:
        """
        for i in range(len(self.board_list)):
            self.board_list[i], score = self.rowLeftOperator(self.board_list[i], score)
        return score

    def moveRight(self, score):
        """
        向右移动
        :return:
        """
        # 左转两次
        self.turnLeft()
        self.turnLeft()
        # 向左操作
        score = self.moveLeft(score)
        # 右转两次
        self.turnRight()
        self.turnRight()
        return score

    def rowLeftOperator(self, row, score):
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
                    score = score + temp[i] * 2
                    flag = False
                else:
                    new_row.append(temp[i])
            else:
                flag = True
        # 补齐
        n = len(row)
        for i in range(n - len(new_row)):
            new_row.append('')
        return new_row, score

    def turnRight(self):
        """
         顺时针旋转90度
        :return:
        """
        # zip()函数对矩阵进行转置
        # item[::-1]对一行进行反转
        self.board_list = [list(x[::-1]) for x in zip(*self.board_list)]

    def turnLeft(self):
        """
        逆时针旋转90度
        :return:
        """
        # 逆时针旋转90度等于顺时针旋转270度
        for i in range(3):
            self.turnRight()

    def checkWin(self):
        """
        判断游戏是否赢
        :return:
        """
        self.board_empty = []
        for i in range(len(self.board_list)):
            for j in range(len(self.board_list[i])):
                if self.board_list[i][j] == 65536:
                    return True
                if self.board_list[i][j] == '':
                    self.board_empty.append((i, j))
        return False

    def checkLose(self):
        """
        判断游戏是否输
        :return:
        """
        if not self.board_empty:
            # 判断每行每列没有相邻的相等元素
            # 判断每一行
            for i in range(len(self.board_list)):
                for j in range(len(self.board_list[i]) - 1):
                    if self.board_list[i][j] == self.board_list[i][j + 1]:
                        return False
            # 判断每一列
            # 先右转90度
            self.turnRight()
            # 再进行判断
            for i in range(len(self.board_list)):
                for j in range(len(self.board_list[i]) - 1):
                    if self.board_list[i][j] == self.board_list[i][j + 1]:
                        # 左转回去
                        self.turnLeft()
                        return False
            return True
        return False
