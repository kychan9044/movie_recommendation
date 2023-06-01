#####
#
# Home UI
#
# requirements:
#   conda install -c conda-forge qtmodern
#
#####
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import QObject, pyqtSignal,Qt, QPoint, QPropertyAnimation, QSize
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QColor
import qtmodern.styles
import qtmodern.windows

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
TOP_WIDTH = WINDOW_WIDTH
TOP_HEIGHT = 80
BODY_WIDTH = WINDOW_WIDTH
BODY_HEIGHT = 1
BODY_EXPAND_HEIGHT = 400

class Signal(QObject):
    click_cb = pyqtSignal()

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("3조-우리집에서영화보고갈래?")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.put_center()

        main_layout = QBoxLayout(QBoxLayout.TopToBottom)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignTop)

        self.event_handler = Signal()

        top = TopLayout(self, self.event_handler)
        top.setFixedSize(TOP_WIDTH, TOP_HEIGHT)
        main_layout.addWidget(top)

        body = BodyLayout(self, self.event_handler)
        body.resize(BODY_WIDTH, BODY_HEIGHT)
        body.move(0, 60)

        top.raise_()

        self.setLayout(main_layout)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        self.setGraphicsEffect(shadow)

        self.show()

    def put_center(self):
        window_geometry = self.frameGeometry()
        desktop_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(desktop_center)
        self.move(window_geometry.topLeft())

class TopLayout(QWidget):
    def __init__(self, parent, event_handler):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.event_handler = event_handler
        self.init_UI()

    def init_UI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("top-layout")
        color = QColor(241, 246, 250, 255)
        shadow = color.darker(115).name()
        self.setStyleSheet(f'''QWidget#top-layout{{
                        background-color: rgba(241, 246, 250, 100%);
                        border-radius: 20px;
                        border-bottom: 3px solid {shadow};
                        padding: 0px;
                        margin: 0px;
                        }}''')
        self.top_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(self.top_layout)
        self.top_layout.setContentsMargins(0,0,0,0)
        self.top_layout.setAlignment(Qt.AlignTop)

        self.button = QPushButton()
        self.button.setObjectName("search-button")
        color = QColor(241, 243, 244, 255)
        shadow = color.darker(115).name()
        self.button.setStyleSheet(f'''#search-button{{
                        background-color: rgba(241, 243, 244, 100%);
                        border-radius: 20px;
                        border: 3px solid {shadow};
                        padding: 0px;
                        margin: 0px;
                        }}''')
        self.button.setFixedSize(80,80)
        self.button.clicked.connect(self.call_click_cb)
        self.add_widget(self.button)

    def call_click_cb(self):
        self.event_handler.click_cb.emit()

    def add_widget(self,widget):
        self.top_layout.addWidget(widget)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
        self.oldPos = event.globalPos()

class BodyLayout(QWidget):
    def __init__(self, parent, event_handler):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.event_handler = event_handler
        self.init_UI()

    def init_UI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("body-layout");
        self.setStyleSheet(f'''#body-layout{{
                background-color: rgba(241, 246, 250, 100%);
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                }}''')
        self.body_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.body_layout)
        self.body_layout.setContentsMargins(0,0,0,0)
        # self.installEventFilter(self)
        self.event_handler.click_cb.connect(self.expend_size)
        self.animation = None

    def expend_size(self):
        if (self.animation != None):
            self.animation.stop()
            self.animation.deleteLater()
            self.animation = None
        self.animation = QPropertyAnimation(self, b'size')
        self.animation.setDuration(100)
        self.animation.setStartValue(QSize(self.width(), BODY_HEIGHT))
        self.animation.setEndValue(QSize(self.width(), BODY_EXPAND_HEIGHT))
        self.animation.start()


    def reduce_size(self):
        if (self.animation != None):
            self.animation.stop()
            self.animation.deleteLater()
            self.animation = None
        self.animation = QPropertyAnimation(self, b'size')
        self.animation.setDuration(100)
        self.animation.setStartValue(QSize(self.width(), BODY_EXPAND_HEIGHT))
        self.animation.setEndValue(QSize(self.width(), BODY_HEIGHT))
        self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.light(app)
    home = Home()
    sys.exit(app.exec_())