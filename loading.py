# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QMovie


class Loading(QtWidgets.QWidget):
    """
    遮盖层
    """
    def __init__(self, parent, tip=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(51,51,51,0.9);')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.parent = parent

        layout = QtWidgets.QVBoxLayout()
        layout.addStretch()

        self.label_gif = QtWidgets.QLabel()
        self.label_gif.setStyleSheet("background:rgba(0,0,0,0);")
        self.label_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.movie = QMovie('image/loading.gif')
        self.movie.setScaledSize(QtCore.QSize(80, 80))
        self.label_gif.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(self.label_gif)

        self.label_tip = QtWidgets.QLabel()
        self.label_tip.setText(tip)
        self.label_tip.setStyleSheet("background:rgba(0,0,0,0);font-size: 18px; color: #FFFFFF; font-weight: 400; "
                                     "font-family: \"思源黑体 CN Regular\";")
        self.label_tip.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_tip)

        layout.addStretch()
        self.setLayout(layout)
        self.show()

    def show(self):
        """重写show，设置遮罩大小与parent一致
        """
        parent_rect = self.parent.geometry()
        self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        super().show()

    def close_loading(self):
        self.deleteLater()

    def modify_tip(self, tip):
        self.label_tip.setText(tip)


class UpdateFirmwareLoading(Loading):
    """
    升级固件进度等待框
    """
    def __init__(self, parent, stage):
        super(UpdateFirmwareLoading, self).__init__(parent, stage)
        self.stage = stage
        self.update_stage(stage)

    def update_stage(self, stage):
        """
        更新阶段
        """
        self.stage = stage
        self.modify_tip(self.stage)

    def update_tip(self, text):
        """
        更新提示
        """
        self.modify_tip(f"{self.stage}{text}")
