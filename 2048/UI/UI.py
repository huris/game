#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QPushButton, QGridLayout, QFrame, QVBoxLayout, QHBoxLayout, QWidget, \
    QApplication

from Constant import VALUE_COLOR_DEF


class UI(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化变量
        self.cell = dict()  # 存储全部像素点组件
        self.cells = list()  # 存储全部的像素点位置,单单存位置

        self.maxScore = 0  # 最高得分
        self.nowScore = 0  # 当前得分

        # 定义一个垂直部件,Floor为整体布局
        self.Floor = QVBoxLayout()

        # 设置一个水平子布局
        self.box = QHBoxLayout()

        # 添加一个重置按钮
        self.restartButton = QPushButton('开始游戏')

        # 定义一个框架
        self.Form = QFrame()

        # 建立一个网格布局
        self.grid = QGridLayout()

        # 添加一个历史最高分数
        self.maxScoreButton = QPushButton('最高分数\n' + str(self.maxScore))

        # 添加一个当前分数
        self.nowScoreButton = QPushButton('当前分数\n' + str(self.nowScore))

        # 建立UI界面
        self.setupUI()

    def changeUI(self, board):
        """
        每移动一步,修改界面
        :return:
        """
        self.nowScoreButton.setText("当前分数\n" + str(self.nowScore))
        self.printBoard(board)


    def setupUI(self):
        """
        设置启动界面的UI
        :return:
        """
        # 设置窗口大小为400*500
        self.resize(400, 500)
        # 将窗口位置居中
        self.centerWindow()
        # 固定窗口大小
        self.setFixedSize(self.width(), self.height())
        # 禁止页面最大化
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        # 设置窗口标题
        self.setWindowTitle('2048')

        # 制作游戏背景的矩形
        self.backGround()

        # 设置2048图标
        self.lbt = QLabel(self)
        self.lbt.setGeometry(20, 108, 360, 360)
        self.pic = QPixmap('image/2048.png')
        self.lbt.setPixmap(self.pic)
        self.lbt.setScaledContents(True)

        self.show()

    def backGround(self):
        """
        绘制矩形界面
        :return:
        """
        # 将那个box部件放到Floor布局中
        self.Floor.addLayout(self.box)

        # 显示最高分数
        self.showMaxScore()

        # 显示当前分数
        self.showNowScore()

        # 设置重置按钮
        self.restartButton.setFixedHeight(50)
        self.restartButton.setFont(QFont('微软雅黑', 15))
        self.restartButton.setStyleSheet(
            "QPushButton{color:rgb(255,255,255);background:rgb(64,116,52);border-radius:8px;}")
        self.box.addWidget(self.restartButton)  # 将重置按钮添加到box布局中

        # 设置框架的形状
        self.Form.setFrameShape(QFrame.Panel | QFrame.Plain)
        self.Form.setStyleSheet("QFrame{background:rgb(205,184,155);border-radius:3px;}")
        # 定义框架的大小
        self.Form.setFixedSize(360, 360)  # 293

        # 设置网格步长
        self.grid.setSpacing(10)

        # 将网格布局添加到Form1中
        self.Form.setLayout(self.grid)
        # 将Form添加到整体的页面中
        self.Floor.addWidget(self.Form)

        # 设置布局为Floor
        self.setLayout(self.Floor)

    def showMaxScore(self):
        """
        显示最高分数
        :return:
        """
        self.maxScoreButton.setFixedHeight(50)
        self.maxScoreButton.setFont(QFont('微软雅黑', 15))
        self.maxScoreButton.setStyleSheet(
            "QPushButton{color:rgb(255,255,255);background:rgb(254,215,0);border-radius:8px;}")
        self.box.addWidget(self.maxScoreButton)

    def showNowScore(self):
        """
        显示当前分数
        :param nowScore:
        :return:
        """
        self.nowScoreButton.setFixedHeight(50)
        self.nowScoreButton.setFont(QFont('微软雅黑', 15))
        self.nowScoreButton.setStyleSheet(
            "QPushButton{color:rgb(252,235,215);background:rgb(204,195,180);border-radius:8px;}")
        self.box.addWidget(self.nowScoreButton)

    def printBoard(self, board_list):
        """
        打印矩形
        :return:
        """
        for row in range(4):
            for col in range(4):
                # 通过QLabel生成像素点
                index = board_list[row][col] if board_list[row][col] != '' else 0
                self.cell[(row, col)] = QLabel(str(index) if index != 0 else '')
                # 设置QSS
                backgroundColor = VALUE_COLOR_DEF[index]
                self.cell[(row, col)].setStyleSheet("QLabel{background:" + backgroundColor + ";}"
                                                    "QLabel{color:rgb(255,255,255);font-size:40px;font-weight:bold;}"
                                                    )
                self.cell[(row, col)].setAlignment(Qt.AlignCenter)
                # 设置一个像素块的大小
                self.cell[(row, col)].setFixedSize(77, 77)
                # 将像素添加到网格布局中
                self.grid.addWidget(self.cell[(row, col)], row, col)
                # 将像素添加到列表中
                self.cells.append((row, col))

    # 调用centerWindow函数,将窗口的位置放在屏幕中央
    def centerWindow(self):
        # 获取屏幕分辨率
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口大小
        size = self.geometry()
        # 移动窗口位置
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
