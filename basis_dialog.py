# -*- coding: utf-8 -*-
import threading
from PySide2.QtCore import Qt
from PySide2 import QtWidgets, QtCore


class MaskWidget(QtWidgets.QWidget):
    """
    遮盖层
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(51,51,51,0.9);')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.parent = parent

    def show(self):
        """重写show，设置遮罩大小与parent一致
        """
        parent_rect = self.parent.geometry()
        self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        super().show()


class CustomDialog(QtWidgets.QDialog):
    """
    自定义弹框
    """
    def __init__(self, content_layout_custom=False):
        super(CustomDialog, self).__init__()
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉原始窗口
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        self.mask = None
        self.self_mask = None   # 多层弹框时使用

        self.width = 400
        self.height = 260
        widget_main = QtWidgets.QWidget()
        widget_main.setObjectName("main-widget")
        widget_main.setStyleSheet("#main-widget{background-color: #FFFFFF; border-radius: 10px;}")

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setMargin(0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        # 头部-------------------
        self.label_title = QtWidgets.QLabel("系统提示")
        self.label_title.setStyleSheet("font-size: 22px; font-family: \"思源黑体 CN Medium\"; font-weight: 500; "
                                       "color: #333333; margin-top: 5px;")
        self.label_title.setAlignment(Qt.AlignHCenter)
        self.btn_close = QtWidgets.QPushButton("")
        self.btn_close.setStyleSheet(f"border-image: url(./image/alert_close.png);")
        self.btn_close.setFixedSize(40, 40)

        layout_head = QtWidgets.QHBoxLayout()
        layout_head.setContentsMargins(40, 0, 10, 0)
        layout_head.addWidget(self.label_title)
        layout_head.addWidget(self.btn_close)
        layout_main.addSpacing(15)
        layout_main.addLayout(layout_head)

        # 分割线------------------
        line = QtWidgets.QLabel()
        line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)
        line.setFixedHeight(1)
        line.setStyleSheet("border: 1px solid #EEEEEE;")
        layout_main.addSpacing(10)
        layout_main.addWidget(line)

        if not content_layout_custom:
            layout_main.addStretch()

        # 中间内容-----------------
        self.layout_content = QtWidgets.QVBoxLayout()
        layout_main.addLayout(self.layout_content)

        # 按钮------------------
        self.layout_btn = QtWidgets.QHBoxLayout()

        if not content_layout_custom:
            layout_main.addStretch()

        layout_main.addLayout(self.layout_btn)
        layout_main.addSpacing(20)

        widget_main.setLayout(layout_main)
        box = QtWidgets.QVBoxLayout()
        box.addWidget(widget_main)
        box.setMargin(0)
        box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(box)

    def reset_dialog_size(self, width, height):
        self.width = width
        self.height = height
        self.setFixedSize(self.width, self.height)

    def add_mask(self, parent):
        self.mask = MaskWidget(parent)
        self.mask.show()

    def set_position_center(self, parent):
        x = parent.x() + parent.width() / 2 - self.width / 2
        y = parent.y() + parent.height() / 2 - self.height / 2
        self.move(x, y)

    def remove_mask(self):
        if self.mask is None:
            return
        else:
            self.mask.close()

    def add_operation(self, btn_list, default_select_btn):
        style = "height: 44px; background: #F5F5F5; border-radius: 6px; border: 1px solid #DDDDDD; " \
                "font-size: 20px; font-family: \"思源黑体 CN Regular\"; font-weight: 400; color: #666666;"
        select_style = "height: 44px; background: #539BD2; border-radius: 6px; border: 1px solid #539BD2; " \
                       "font-size: 20px; font-family: \"思源黑体 CN Regular\"; font-weight: 400; color: #FFFFFF;"
        self.layout_btn.addStretch()
        self.layout_btn.setSpacing(20)
        for btn in btn_list:
            btn.setFixedWidth(150)
            if btn in default_select_btn:
                btn.setStyleSheet(select_style)
            else:
                btn.setStyleSheet(style)
            self.layout_btn.addWidget(btn)
        self.layout_btn.addStretch()

    def add_self_mask(self, parent=None):
        self.self_mask = MaskWidget(self)
        self.self_mask.show()
        if parent is not None:
            self.remove_mask()

    def remove_self_mask(self, parent=None):
        if self.self_mask is None:
            return
        else:
            self.self_mask.close()

        if parent is not None:
            self.add_mask(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass


class Alert(CustomDialog):
    """
    弹框
    """
    def __init__(self, content: str, btn_text: str = "确认", title: str = "温馨提示", parent=None):
        super(Alert, self).__init__()
        self.parent = parent

        self.reset_dialog_size(300, 220)

        # 标题
        self.label_title.setText(title)

        # 中间内容-----------------
        self.label_content = QtWidgets.QLabel(content)
        self.label_content.adjustSize()
        self.label_content.setStyleSheet("font-size: 18px; color: #666666; font-weight: 400; "
                                         "font-family: \"思源黑体 CN Regular\"; margin: 10px 50px;")
        self.label_content.setWordWrap(True)
        self.label_content.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)  # 文字水平垂直居中
        self.layout_content.addWidget(self.label_content)

        # 按钮-----------------------------
        self.btn = QtWidgets.QPushButton(btn_text)
        self.add_operation([self.btn], [self.btn])

        self.btn.clicked.connect(self.close_dialog)
        self.btn_close.clicked.connect(self.close_dialog)

        if self.parent is not None:
            self.add_mask(self.parent)
            self.set_position_center(self.parent)

        self.exec_()

    def close_dialog(self):
        if self.parent is not None:
            self.remove_mask()
        self.close()


class Tip(QtWidgets.QDialog):
    """
    提示框
    """
    def __init__(self, content, show_second=1, parent=None, width=100):
        super(Tip, self).__init__()
        self.setWindowModality(Qt.NonModal)  # 应用程序模态
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉原始窗口
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明

        self.setFixedSize(width, 50)

        widget_main = QtWidgets.QWidget()
        widget_main.setObjectName("main-widget")
        widget_main.setStyleSheet("#main-widget{background-color: #696969; border-radius: 6px;}")

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setMargin(0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        # 头部-------------------
        self.label_title = QtWidgets.QLabel(content)
        self.label_title.setStyleSheet("font-size: 18px; font-family: \"思源黑体 CN Medium\"; color: #FFFFFF;")
        self.label_title.setAlignment(Qt.AlignCenter)
        layout_main.addWidget(self.label_title)

        widget_main.setLayout(layout_main)
        box = QtWidgets.QVBoxLayout()
        box.addWidget(widget_main)
        box.setMargin(0)
        box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(box)
        if parent is not None:
            self.set_position_center(parent)

        self.show()

        timer = threading.Timer(show_second, self.close_dialog)
        timer.start()

    def close_dialog(self):
        self.close()

    def set_position_center(self, parent):
        x = parent.x() + parent.width() / 2 - self.size().width() / 2
        y = parent.y() + parent.height() / 2 - self.size().height() / 2
        self.move(x, y)
