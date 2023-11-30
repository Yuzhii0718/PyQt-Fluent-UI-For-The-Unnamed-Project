# coding:utf-8
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('欢迎来到 Home_interface.', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            ':/gallery/images/logo.png',
            self.tr('开始上手'),
            self.tr('应用程序开发选项和示例的概述'),
            HELP_URL
        )

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub repo'),
            self.tr(
                '进入项目的 Github 主页，查看源码，提交 issue 和 pull request'),
            REPO_URL
        )

        self.linkCardView.addCard(
            FluentIcon.CODE,
            self.tr('代码示例'),
            self.tr(
                '查找演示特定任务、功能和 API 的示例'),
            EXAMPLE_URL
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            self.tr('发送反馈'),
            self.tr('通过你的反馈帮助我们改进产品'),
            FEEDBACK_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """ load samples """
        # introduction samples
        introductionView = SampleCardView(
            self.tr('介绍'), self.view)
        introductionView.addSampleCard(
            icon=":/gallery/images/controls/CommandBarFlyout.png",
            title="功能 A",
            content=self.tr(
                "这是功能 A 的介绍文字"),
            routeKey="",
            index=0
        )
        introductionView.addSampleCard(
            icon=":/gallery/images/controls/CreateMultipleWindows.png",
            title="功能 B",
            content=self.tr("这是功能 B 的介绍文字"),
            routeKey="",
            index=1
        )
        introductionView.addSampleCard(
            icon=":/gallery/images/controls/Grid.png",
            title="功能 C",
            content=self.tr(
                "这是功能 C 的介绍文字"),
            routeKey="",
            index=2
        )
        introductionView.addSampleCard(
            icon=":/gallery/images/controls/MenuBar.png",
            title="功能 D",
            content=self.tr(
                "这是功能 D 的介绍文字"),
            routeKey="",
            index=3
        )
        self.vBoxLayout.addWidget(introductionView)

        # api samples
        apiView = SampleCardView(
            self.tr('API'), self.view)
        apiView.addSampleCard(
            icon=":/gallery/images/controls/NavigationView.png",
            title="API A",
            content=self.tr(
                "这是 API A 的介绍文字"),
            routeKey="",
            index=0
        )
        self.vBoxLayout.addWidget(apiView)

        # opensource samples
        self.opensourceView = SampleCardView(
            self.tr('开放源代码'), self.view)
        self.opensourceView.addSampleCard(
            icon=":/gallery/images/controls/AnimationInterop.png",
            title="PyQt-Fluent-Widgets",
            content=self.tr(
                "由 zhiyiYo 构建 PyQt5 的 Fluent UI 风格的组件库"),
            routeKey="https://github.com/zhiyiYo/PyQt-Fluent-Widgets",
            index=0
        )
        self.opensourceView.addSampleCard(
            icon=":/gallery/images/controls/AnimationInterop.png",
            title="开源 B",
            content=self.tr("使用 开源 B 的介绍文字"),
            routeKey="",
            index=1
        )
        self.vBoxLayout.addWidget(self.opensourceView)

        # Deverloper samples
        developerView = SampleCardView(
            self.tr('开发者'), self.view)
        developerView.addSampleCard(
            icon=":/gallery/images/controls/PersonPicture.png",
            title="开发者 A",
            content=self.tr(
                "开发者 A 的介绍文字"),
            routeKey="",
            index=0
        )
        developerView.addSampleCard(
            icon=":/gallery/images/controls/PersonPicture.png",
            title="开发者 B",
            content=self.tr("开发者 B 的介绍文字"),
            routeKey="",
            index=1
        )
        developerView.addSampleCard(
            icon=":/gallery/images/controls/PersonPicture.png",
            title="开发者 C",
            content=self.tr(
                "开发者 C 的介绍文字"),
            routeKey="",
            index=2
        )
        self.vBoxLayout.addWidget(developerView)

    def openWebsite(self, url):
        import webbrowser
        webbrowser.open(url)
