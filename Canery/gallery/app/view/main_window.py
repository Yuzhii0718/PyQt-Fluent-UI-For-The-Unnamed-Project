# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices, QColor, QCursor
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen, setFont)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (RoundMenu, FluentIcon, Action, AvatarWidget, BodyLabel,
                            HyperlinkButton, CaptionLabel, setFont, setTheme, Theme, isDarkTheme)
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .basic_input_interface import BascInputInterface
from .date_time_interface import DateTimeInterface
from .dialog_interface import DialogInterface
from .layout_interface import LayoutInterface
from .panel_interface import PanelInterface

from .setting_interface import SettingInterface

from ..common.config import SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource


class ProfileCard(QWidget):
    """ Profile card """

    def __init__(self, avatarPath: str, name: str, email: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.emailLabel = CaptionLabel(email, self)
        self.logoutButton = HyperlinkButton(
            'https://example.com', '注销', self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.emailLabel.setStyleSheet('QLabel{color: ' + color.name() + '}')

        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: ' + color.name() + '}')
        setFont(self.logoutButton, 13)

        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.emailLabel.move(64, 32)
        self.logoutButton.move(52, 48)


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        # 创建子界面
        self.homeInterface = HomeInterface(self)
        self.panelInterface = PanelInterface(self)
        self.basicInputInterface = BascInputInterface(self)
        self.dateTimeInterface = DateTimeInterface(self)
        self.dialogInterface = DialogInterface(self)
        self.layoutInterface = LayoutInterface(self)
        # self.menuInterface = MenuInterface(self)
        # self.materialInterface = MaterialInterface(self)
        # self.navigationViewInterface = NavigationViewInterface(self)
        # self.scrollInterface = ScrollInterface(self)
        # self.statusInfoInterface = StatusInfoInterface(self)
        self.settingInterface = SettingInterface(self)
        # self.textInterface = TextInterface(self)
        # self.viewInterface = ViewInterface(self)

        # enable acrylic effect
        # 启用亚克力效果
        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        # add items to navigation interface
        # 添加导航项
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        # signalBus.supportSignal.connect(self.onSupport)
        signalBus.supportSignal.connect(self.showProfileCard)

    def initNavigation(self):
        # add navigation items
        # 添加导航项
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('主页'))
        self.addSubInterface(self.panelInterface, Icon.EMOJI_TAB_SYMBOLS, t.panel)
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.basicInputInterface, FIF.TILES, t.basicInput, pos)
        self.addSubInterface(self.dateTimeInterface, FIF.TILES, t.dateTime, pos)
        self.addSubInterface(self.dialogInterface, FIF.TILES, t.dialogs, pos)
        self.addSubInterface(self.layoutInterface, FIF.TILES, t.layout, pos)
        # self.addSubInterface(self.materialInterface, FIF.PALETTE, t.material, pos)
        # self.addSubInterface(self.menuInterface, Icon.MENU, t.menus, pos)
        # self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos)
        # self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)
        # self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos)
        # self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)
        # self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)

        # add custom widget to bottom
        # 添加自定义控件到底部
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Yuzhii0718', ':/gallery/images/avatar.png'),
            onClick=self.showProfileCard,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('设定'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets Main Demo')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        w = MessageBox(
            '关于我们',
            '开发不易，希望这个项目帮助到了您。',
            self
        )
        w.yesButton.setText('谢谢')
        w.cancelButton.setText('关闭')
        if w.exec():
            # QDesktopServices.openUrl(QUrl(SUPPORT_URL))
            pass

    def showProfileCard(self):
        menu = RoundMenu(parent=self)

        # add custom widget
        card = ProfileCard(':/gallery/images/avatar.png', 'Yuzhii', 'example@outlook.com', menu)
        menu.addWidget(card, selectable=False)
        # menu.addWidget(card, selectable=True, onClick=lambda: print('666'))
        try:
            menu.addSeparator()
            menu.addActions([
                Action(FluentIcon.PEOPLE, '管理账户和设置'),
                Action(FluentIcon.SHOPPING_CART, '功能 A'),
                Action(FluentIcon.CODE, '功能 B'),
            ])
            menu.addSeparator()
            actionInfo = Action(FluentIcon.INFO, '关于')
            actionInfo.triggered.connect(self.onSupport)
            menu.addAction(actionInfo)

            menu.exec(QCursor.pos())
        except Exception as e:
            print(e)
            pass

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
