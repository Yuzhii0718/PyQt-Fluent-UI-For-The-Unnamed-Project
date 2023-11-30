# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 22:40
# @Author  : Yuzhii0718
# @File    : main.py
# @Software: PyCharm

# coding:utf-8
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar

from app.common.config import cfg
from app.view.main_window import MainWindow

from app.view.login.Ui_LoginWindow import Ui_Form


class LoginWindow(AcrylicWindow, Ui_Form):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('PyQt-Fluent-Widget Login Demo')
        self.setWindowIcon(QIcon(":/gallery/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.setStyleSheet("LoginWindow{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""QLabel{
            background: transparent;
            font: 13px 'Segoe UI';
            padding: 0 4px;
            color: white
        }""")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.label_2.setPixmap(QtGui.QPixmap(":/gallery/images/logo.png"))
        self.pushButton.clicked.connect(self.enterApp)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/gallery/images/background.png").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def enterApp(self):
        self.hide()
        self.main_window.show()


if __name__ == '__main__':
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # 创建主窗口但不显示
    main_window = MainWindow()
    main_window.hide()

    # 创建并显示登录窗口
    login_window = LoginWindow(main_window)
    login_window.show()

    app.exec_()
