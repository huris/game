#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QFrame, QGridLayout, QPushButton, QLCDNumber, QLabel, \
    QVBoxLayout, QHBoxLayout, QMessageBox

from Board import Board
from UI import UI


class Game(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.board = Board()  # 建立board
        self.ui = UI()  # 建立UI
        self.ui.restartButton.clicked.connect(self.start)  # 连接槽函数
        self.grabKeyboard()  # 窗口接受键盘事件

        # 开始游戏
        self.start()

    def start(self):
        """
        开始游戏
        :return:
        """
        # 建立Board
        self.board = Board()

        # 建立UI界面
        self.ui = UI()

    # 设置键盘响应操作
    def keyPressEvent(self, event):  # 响应键盘操作
        if event.key() == Qt.Key_Left:
            self.ui.nowScore = self.board.moveLeft(self.ui.nowScore)
        if event.key() == Qt.Key_Right:
            self.ui.nowScore = self.board.moveRight(self.ui.nowScore)
        if event.key() == Qt.Key_Up:
            self.ui.nowScore = self.board.moveUp(self.ui.nowScore)
        if event.key() == Qt.Key_Down:
            self.ui.nowScore = self.board.moveDown(self.ui.nowScore)
        # 校检
        self.check()

    def check(self):
        """
        每次移动完都要进行判断
        :return:
        """
        # 判断一下是否赢了
        if self.isWin():
            self.QMS = QMessageBox.information(self,
                                               'YOU WIN',
                                               '成功的人\n决不步人后尘\n而是永不放弃,创新!\n希望你能更上一层楼!',
                                               QMessageBox.Ok)
            self.start()
        # 判断是否输了
        elif self.isLose():
            self.QMS = QMessageBox.information(self,
                                               'YOU LOSE',
                                               '只有经历过失败才是真正的赢\n因为你吸取了失败的教训,懂得了失败的真谛\n别灰心,再接再励!',
                                               QMessageBox.Ok)
            self.start()
        else:
            # 修改当前分数
            self.ui.changeUI(self.board.board_list)
            # 在空白的地方,随机添加2,4
            self.board.addPiece()

    def isWin(self):
        # 判断游戏是否赢了
        # 空位也要找出来
        return self.board.checkWin()

    def isLose(self):
        # 判断是否输了
        return self.board.checkLose()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
