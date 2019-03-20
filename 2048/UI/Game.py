#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget
from Board import Board
from UI import UI


class Game(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.isStart = False  # 控制键盘
        self.nowScore = 0  # 当前得分
        # 最高得分从文件夹中获取
        with open('maxScore.txt', 'r') as f:
            self.maxScore = int(f.readline())  # 最高得分

        self.grabKeyboard()  # 窗口接受键盘事件

        # 开始游戏
        self.start()

    def start(self):
        """
        开始游戏
        :return:
        """
        # 重新开始时,当前分数为0
        self.nowScore = 0  # 当前得分

        # 建立Board
        self.board = Board()

        # 建立UI界面
        self.ui = UI()
        self.ui.restartButton.clicked.connect(self.restart)  # 连接槽函数

    def restart(self):
        """
        重新开始
        :return:
        """
        self.start()
        self.ui.changeUI(self.board.board_list, self.nowScore, self.maxScore)  # 刚开始有两个
        self.ui.lbt.close()
        self.ui.restartButton.setText("重新开始")
        self.ui.restartButton.setStyleSheet(
            "QPushButton{color:rgb(255,255,255);background:rgb(247,127,102);border-radius:8px;}")
        self.isStart = True  # 可以开始游戏

    # 设置键盘响应操作
    def keyPressEvent(self, event):  # 响应键盘操作
        if self.isStart == True:
            if event.key() == Qt.Key_Left:
                self.nowScore = self.board.moveLeft(self.nowScore)
            if event.key() == Qt.Key_Right:
                self.nowScore = self.board.moveRight(self.nowScore)
            if event.key() == Qt.Key_Up:
                self.nowScore = self.board.moveUp(self.nowScore)
            if event.key() == Qt.Key_Down:
                self.nowScore = self.board.moveDown(self.nowScore)
            # 校检
            self.check()

    def check(self):
        """
        每次移动完都要进行判断
        :return:
        """
        # 判断一下是否赢了
        if self.isWin():
            self.isStart = False
            self.QMS = QMessageBox.information(self,
                                               'YOU WIN',
                                               '成功的人\n决不步人后尘\n而是永不放弃,创新!\n希望你能更上一层楼!',
                                               QMessageBox.Ok)
            self.start()
        # 判断是否输了
        elif self.isLose():
            self.isStart = False
            self.QMS = QMessageBox.information(self,
                                               'YOU LOSE',
                                               '只有经历过失败才是真正的赢\n因为你吸取了失败的教训,懂得了失败的真谛\n别灰心,再接再励!',
                                               QMessageBox.Ok)
            self.start()
        else:
            # 在空白的地方,随机添加2,4
            self.board.addPiece()
            # 修改当前分数
            self.ui.changeUI(self.board.board_list, self.nowScore, self.maxScore)

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
