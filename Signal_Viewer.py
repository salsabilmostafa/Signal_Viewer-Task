
from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QMainWindow, QTableWidgetItem, QLineEdit
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import pyqtgraph.exporters
from PyQt5.QtCore import QTimer
import numpy as np
import pandas as pd
from fpdf import FPDF
import os
import statistics
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import random
from pyqtgraph import ViewBox, RectROI
from pyqtgraph.Qt import QtCore


class ColorSelectionDialog(QDialog):
    color_selected = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(ColorSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Point Color")

        self.color = QColor(0, 0, 255)  # Initial color (blue)

        self.color_button = QtWidgets.QPushButton(self)
        self.color_button.setGeometry(QtCore.QRect(50, 20, 100, 30))
        self.color_button.setText("Select Color")
        self.color_button.clicked.connect(self.open_color_dialog)

    def open_color_dialog(self):
        color = QColorDialog.getColor(self.color, self, "Select Point Color")
        if color.isValid():
            self.color = color
            # Update the color of the plotted points
            self.color_selected.emit(color)


class ColorSelectionDialog2(QDialog):
    color_selected2 = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(ColorSelectionDialog2, self).__init__(parent)
        self.setWindowTitle("Select Point Color (Widget)")

        self.color2 = QColor(0, 0, 255)  # Initial color (blue)

        self.color_button2 = QtWidgets.QPushButton(self)
        self.color_button2.setGeometry(QtCore.QRect(50, 20, 100, 30))
        self.color_button2.setText("Select Color")
        self.color_button2.clicked.connect(self.open_color_dialog2)

    def open_color_dialog2(self):
        color2 = QColorDialog.getColor(
            self.color2, self, "Select Point Color (Right_Graph)")
        if color2.isValid():
            self.color2 = color2
            self.color_selected2.emit(color2)


x_values = []
y_values = []
x_values_LGraph = []
y_values_LGraph = []


def get_random_color():

    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return (red, green, blue)


class Ui_MainWindow(object):
    point_color = QColor(0, 0, 255)
    point_color2 = QColor(255, 0, 0)
    MAX_X_RANGE = 100
    dynamic_iteration = 0
    test = []
    Xcoordinates = []
    Xplotted = 0
    Xplotted2 = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1011, 656)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("\n"
                                 "background-color: rgb(231, 231, 231);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet("background-color: rgb(213, 213, 213);\n"
                                 "border-right-color: rgb(139, 139, 139);\n"
                                 "border-color: rgb(118, 118, 118);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")

        self.ZoomIn_Button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ZoomIn_Button_Left.sizePolicy().hasHeightForWidth())
        self.ZoomIn_Button_Left.setSizePolicy(sizePolicy)
        self.ZoomIn_Button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.ZoomIn_Button_Left.setObjectName("ZoomIn_Button_Left")
        self.gridLayout.addWidget(self.ZoomIn_Button_Left, 1, 0, 1, 1)

        self.ZoomOut_Button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ZoomOut_Button_Left.sizePolicy().hasHeightForWidth())
        self.ZoomOut_Button_Left.setSizePolicy(sizePolicy)
        self.ZoomOut_Button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.ZoomOut_Button_Left.setObjectName("ZoomOut_Button_Left")
        self.gridLayout.addWidget(self.ZoomOut_Button_Left, 1, 2, 1, 1)

        self.Start_Stop_Button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Start_Stop_Button_Left.sizePolicy().hasHeightForWidth())
        self.Start_Stop_Button_Left.setSizePolicy(sizePolicy)
        self.Start_Stop_Button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179)")
        self.Start_Stop_Button_Left.setObjectName("pushButton")
        self.gridLayout.addWidget(self.Start_Stop_Button_Left, 0, 1, 1, 2)

        self.ChangeColor_Button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ChangeColor_Button_Left.sizePolicy().hasHeightForWidth())
        self.ChangeColor_Button_Left.setSizePolicy(sizePolicy)
        self.ChangeColor_Button_Left.setStyleSheet(
            " background-color:rgb(179, 179, 179)")
        self.ChangeColor_Button_Left.setObjectName("ChangeColor_Button_Left")
        self.gridLayout.addWidget(self.ChangeColor_Button_Left, 1, 3, 1, 3)

        self.horizontalSlider = QtWidgets.QSlider(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 3, 3, 1, 3)

        self.Speed_Label_Left = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Speed_Label_Left.sizePolicy().hasHeightForWidth())
        self.Speed_Label_Left.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.Speed_Label_Left.setFont(font)
        self.Speed_Label_Left.setAlignment(QtCore.Qt.AlignCenter)
        self.Speed_Label_Left.setObjectName("label")
        self.gridLayout.addWidget(self.Speed_Label_Left, 2, 3, 1, 3)

        self.hide_button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.hide_button_Left.sizePolicy().hasHeightForWidth())
        self.hide_button_Left.setSizePolicy(sizePolicy)
        self.hide_button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.hide_button_Left.setObjectName("hide_button_Left")
        self.gridLayout.addWidget(self.hide_button_Left, 2, 0, 1, 3)

        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 3, 1, 1, 2)

        self.Label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(10)
        self.Label.setFont(font)
        self.Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Label.setObjectName("label_2")
        self.gridLayout.addWidget(self.Label, 3, 0, 1, 1)

        self.Browse_button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Browse_button_Left.sizePolicy().hasHeightForWidth())
        self.Browse_button_Left.setSizePolicy(sizePolicy)
        self.Browse_button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Browse_button_Left.setObjectName("Browse_button_Left")
        self.gridLayout.addWidget(self.Browse_button_Left, 5, 5, 1, 1)

        self.ComboBox_Left = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ComboBox_Left.sizePolicy().hasHeightForWidth())
        self.ComboBox_Left.setSizePolicy(sizePolicy)
        self.ComboBox_Left.setObjectName("ComboBox_Left")
        self.gridLayout.addWidget(self.ComboBox_Left, 4, 1, 1, 2)
        self.gridLayout_3.addWidget(self.frame, 3, 0, 1, 2)

        self.select_channel_label_Left = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.select_channel_label_Left.sizePolicy().hasHeightForWidth())
        self.select_channel_label_Left.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        self.select_channel_label_Left.setFont(font)
        self.select_channel_label_Left.setAlignment(QtCore.Qt.AlignCenter)
        self.select_channel_label_Left.setObjectName(
            "select_channel_label_Left")
        self.gridLayout.addWidget(self.select_channel_label_Left, 4, 0, 1, 1)

        self.Print_button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Print_button_Left.sizePolicy().hasHeightForWidth())
        self.Print_button_Left.setSizePolicy(sizePolicy)
        self.Print_button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Print_button_Left.setObjectName("Print_button_Left")
        self.gridLayout.addWidget(self.Print_button_Left, 4, 5, 1, 1)

        self.Snap_button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Snap_button_Left.sizePolicy().hasHeightForWidth())
        self.Snap_button_Left.setSizePolicy(sizePolicy)
        self.Snap_button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Snap_button_Left.setObjectName("Snap_button_Left")
        self.gridLayout.addWidget(self.Snap_button_Left, 5, 3, 1, 1)

        self.MoveToGraph2_Button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.MoveToGraph2_Button.sizePolicy().hasHeightForWidth())
        self.MoveToGraph2_Button.setSizePolicy(sizePolicy)
        self.MoveToGraph2_Button.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.MoveToGraph2_Button.setObjectName("MoveToGraph2_Button")
        self.gridLayout.addWidget(self.MoveToGraph2_Button, 5, 0, 1, 3)

        self.Link_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Link_Button.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Link_Button.setObjectName("Link_Button")
        self.gridLayout_3.addWidget(self.Link_Button, 0, 1, 1, 4)

        self.Left_Graph = PlotWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.Left_Graph.setFont(font)
        self.Left_Graph.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.Left_Graph.setObjectName("Left_Graph")
        self.gridLayout_3.addWidget(self.Left_Graph, 1, 1, 1, 1)
        self.Right_Graph = PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Right_Graph.sizePolicy().hasHeightForWidth())
        self.Right_Graph.setSizePolicy(sizePolicy)
        self.Right_Graph.setObjectName("Right_Graph")
        self.gridLayout_3.addWidget(self.Right_Graph, 1, 4, 1, 1)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("background-color: rgb(213, 213, 213);\n"
                                   "border-right-color: rgb(139, 139, 139);\n"
                                   "border-color: rgb(118, 118, 118);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3.addWidget(self.frame_2, 3, 3, 1, 2)

        self.ZoomIn_Button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ZoomIn_Button_Right.sizePolicy().hasHeightForWidth())
        self.ZoomIn_Button_Right.setSizePolicy(sizePolicy)
        self.ZoomIn_Button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.ZoomIn_Button_Right.setObjectName("ZoomIn_Button_Right")
        self.gridLayout_2.addWidget(self.ZoomIn_Button_Right, 1, 0, 1, 1)

        self.ZoomOut_Button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ZoomOut_Button_Right.sizePolicy().hasHeightForWidth())
        self.ZoomOut_Button_Right.setSizePolicy(sizePolicy)
        self.ZoomOut_Button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.ZoomOut_Button_Right.setObjectName("ZoomOut_Button_Right")
        self.gridLayout_2.addWidget(self.ZoomOut_Button_Right, 1, 1, 1, 1)

        self.Start_Stop_Button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Start_Stop_Button_Right.sizePolicy().hasHeightForWidth())
        self.Start_Stop_Button_Right.setSizePolicy(sizePolicy)
        self.Start_Stop_Button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179)")
        self.Start_Stop_Button_Right.setObjectName("Start_Stop_Button_Right")
        self.gridLayout_2.addWidget(self.Start_Stop_Button_Right, 0, 1, 1, 1)

        self.ChangeColor_Button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ChangeColor_Button_Right.sizePolicy().hasHeightForWidth())
        self.ChangeColor_Button_Right.setSizePolicy(sizePolicy)
        self.ChangeColor_Button_Right.setStyleSheet(
            " background-color:rgb(179, 179, 179)")
        self.ChangeColor_Button_Right.setObjectName("ChangeColor_Button_Right")
        self.gridLayout_2.addWidget(self.ChangeColor_Button_Right, 1, 2, 1, 4)

        self.horizontalSlider_2 = QtWidgets.QSlider(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy)
        self.horizontalSlider_2.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.gridLayout_2.addWidget(self.horizontalSlider_2, 3, 2, 1, 4)

        self.Speed_Label_Right = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Speed_Label_Right.sizePolicy().hasHeightForWidth())
        self.Speed_Label_Right.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("8514oem")
        self.Speed_Label_Right.setFont(font)
        self.Speed_Label_Right.setAlignment(QtCore.Qt.AlignCenter)
        self.Speed_Label_Right.setObjectName("Speed_Label_Right")
        self.gridLayout_2.addWidget(self.Speed_Label_Right, 2, 3, 1, 3)

        self.hide_button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.hide_button_Right.sizePolicy().hasHeightForWidth())
        self.hide_button_Right.setSizePolicy(sizePolicy)
        self.hide_button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.hide_button_Right.setObjectName("hide_button_Right")
        self.gridLayout_2.addWidget(self.hide_button_Right, 2, 0, 1, 2)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 3, 1, 1, 1)

        self.Label_2 = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Label_2.sizePolicy().hasHeightForWidth())
        self.Label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(10)
        self.Label_2.setFont(font)
        self.Label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_2.setObjectName("Text")
        self.gridLayout_2.addWidget(self.Label_2, 3, 0, 1, 1)

        self.Browse_button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Browse_button_Right.sizePolicy().hasHeightForWidth())
        self.Browse_button_Right.setSizePolicy(sizePolicy)
        self.Browse_button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Browse_button_Right.setObjectName("Browse_button_Right")
        self.gridLayout_2.addWidget(self.Browse_button_Right, 5, 5, 1, 1)

        self.ComboBox_Right = QtWidgets.QComboBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.ComboBox_Right.sizePolicy().hasHeightForWidth())
        self.ComboBox_Right.setSizePolicy(sizePolicy)
        self.ComboBox_Right.setObjectName("ComboBox_Right")
        self.gridLayout_2.addWidget(self.ComboBox_Right, 4, 1, 1, 2)

        self.select_channel_label_Right = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.select_channel_label_Right.sizePolicy().hasHeightForWidth())
        self.select_channel_label_Right.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        self.select_channel_label_Right.setFont(font)
        self.select_channel_label_Right.setAlignment(QtCore.Qt.AlignCenter)
        self.select_channel_label_Right.setObjectName(
            "select_channel_label_Right")
        self.gridLayout_2.addWidget(
            self.select_channel_label_Right, 4, 0, 1, 1)

        self.Print_button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Print_button_Right.sizePolicy().hasHeightForWidth())
        self.Print_button_Right.setSizePolicy(sizePolicy)
        self.Print_button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Print_button_Right.setObjectName("Print_button_Right")
        self.gridLayout_2.addWidget(self.Print_button_Right, 4, 5, 1, 1)

        self.MoveToGraph1_Button = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.MoveToGraph1_Button.sizePolicy().hasHeightForWidth())
        self.MoveToGraph1_Button.setSizePolicy(sizePolicy)
        self.MoveToGraph1_Button.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.MoveToGraph1_Button.setObjectName("MoveToGraph1_Button")
        self.gridLayout_2.addWidget(self.MoveToGraph1_Button, 5, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionBrowse = QtWidgets.QAction(MainWindow)
        self.actionBrowse.setObjectName("actionBrowse")
        self.actionBrowse.triggered.connect(self.browsefiles)
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.Speed_Label_Left.setBuddy(self.horizontalSlider)
        self.Speed_Label_Right.setBuddy(self.horizontalSlider)

        self.Rewind_button_Left = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Rewind_button_Left.sizePolicy().hasHeightForWidth())
        self.Rewind_button_Left.setSizePolicy(sizePolicy)
        self.Rewind_button_Left.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Rewind_button_Left.setObjectName("Rewind_button_Left")
        self.gridLayout.addWidget(self.Rewind_button_Left, 0, 3, 1, 2)

        self.Rewind_button_Right = QtWidgets.QPushButton(self.frame_2)
        self.Rewind_button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Rewind_button_Right.setObjectName("Rewind_button_Right1")
        self.gridLayout_2.addWidget(self.Rewind_button_Right, 0, 2, 1, 2)

        self.Snap_button_Right = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.Snap_button_Right.sizePolicy().hasHeightForWidth())
        self.Snap_button_Right.setSizePolicy(sizePolicy)
        self.Snap_button_Right.setStyleSheet(
            "background-color: rgb(179, 179, 179);")
        self.Snap_button_Right.setObjectName("Snap_button_Right")
        self.gridLayout_2.addWidget(self.Snap_button_Right, 5, 3, 1, 1)
        graph_1_control = self.Left_Graph.addLegend()
        graph_2_control = self.Right_Graph.addLegend()

        # array for selected
        self.hidden_data = []
        self.hidden_data2 = []
        self.moved_data = []
        self.moved_data2 = []

        # checks hidden of Left_Graph
        self.hidden = True
        self.hidden2 = True
        self.hidden2_data1 = True
        self.hidden2_data2 = True

        # flag for start_stop
        self.running = True

        # flag for start_stop of widget graph
        self.running2 = True
        self.moved2 = False
        self.moved = False

        # flag for linking
        self.graphs_linked = False
        self.linked_timer = None

        # SPEED
        # playback speed
        self.timer = QTimer()
        self.update_graph_speed(self.horizontalSlider.value())
        self.timer.start(3000)

        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(99)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setPageStep(10)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.valueChanged.connect(
            self.update_Speed_Label_Left)

        self.update_Speed_Label_Left(self.horizontalSlider.value())

        # playback speed widget
        self.timer2 = QTimer()

        self.update_graph_speed_2(self.horizontalSlider_2.value())
        self.timer2.start(3000)

        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(99)
        self.horizontalSlider_2.setSingleStep(1)
        self.horizontalSlider_2.setPageStep(10)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_2.valueChanged.connect(
            self.update_Speed_Label_Right)

        self.update_Speed_Label_Right(self.horizontalSlider_2.value())

        # scroll
        self.horizontalScroller = QtWidgets.QScrollBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(
            self.horizontalScroller .sizePolicy().hasHeightForWidth())
        self.horizontalScroller .setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Kristen ITC")
        self.horizontalScroller .setFont(font)
        self.horizontalScroller .setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScroller .setObjectName("horizontalScroller ")
        self.gridLayout_3.addWidget(self.horizontalScroller, 2, 1, 1, 1)
        self.horizontalScroller.setObjectName("horizontalScroller ")

        self.verticalSlider = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.gridLayout_3.addWidget(self.verticalSlider, 1, 0, 1, 1)
        # Set the minimum and maximum values of the slider
        self.horizontalScroller.setMinimum(0)
        self.horizontalScroller.setMaximum(100)
        self.horizontalScroller.setSingleStep(1)
        self.horizontalScroller.setPageStep(1)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(100)
        self.horizontalScroller.setSingleStep(1)
        self.horizontalScroller.setPageStep(1)
        # Connect the slider value changed signal to a function that updates the x-axis of the graph
        # self.horizontalScroller.valueChanged.connect(self.update_x_axis)
        # self.verticalSlider.valueChanged.connect(self.update_y_axis)
        self.horizontalScroller_2 = QtWidgets.QScrollBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.horizontalScroller_2.sizePolicy().hasHeightForWidth())
        self.horizontalScroller_2.setSizePolicy(sizePolicy)
        self.horizontalScroller_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScroller_2.setObjectName("horizontalScroller_2")
        self.gridLayout_3.addWidget(self.horizontalScroller_2, 2, 4, 1, 1)

        self.horizontalScroller.setSingleStep(1)
        self.horizontalScroller.setPageStep(1)
        self.verticalSlider_2 = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalSlider_2.setGeometry(QtCore.QRect(440, 40, 20, 281))
        self.verticalSlider_2.setStyleSheet(
            "background-color: rgb(231, 231, 231);")
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider")
        self.gridLayout_3.addWidget(self.verticalSlider_2, 1, 2, 1, 2)
        self.horizontalScroller.setSingleStep(1)
        self.horizontalScroller.setPageStep(1)
        # Set the minimum and maximum values of the slider
        self.horizontalScroller_2.setMinimum(0)
        self.horizontalScroller_2.setMaximum(100)
        self.verticalSlider_2.setMinimum(0)
        self.verticalSlider_2.setMaximum(100)

        # selecting channel
        # Create a list to store the file names and data
        self.channels = []
        self.selected_channel = None

        self.channel_names = []
        self.channel_colors = {}

        # widget ComboBox_Left
        self.channels2 = []
        self.selected_channel2 = None

        self.channel_names2 = []
        self.channel_colors2 = {}

        # self.ComboBox_Right.currentIndexChanged.connect(self.select_channel2)

        # creating pdfs
        self.statistics = []
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.snapshots_enabled = False

        # Array to store images for snapshots
        self.images = []

        # creating pdfs
        self.statistics2 = []
        self.pdf2 = FPDF()
        self.pdf2.set_auto_page_break(auto=True, margin=15)
        self.snapshots_enabled2 = False

        # Array to store images for snapshots
        self.images2 = []

        # buttons action
        self.Browse_button_Left.clicked.connect(self.browsefiles)
        self.Browse_button_Right.clicked.connect(self.browsefiles2)
        self.ZoomIn_Button_Left.clicked.connect(self.zoom_in)
        self.ZoomOut_Button_Left.clicked.connect(self.zoom_out)
        self.ZoomIn_Button_Right.clicked.connect(self.zoom_in2)
        self.ZoomOut_Button_Right.clicked.connect(self.zoom_out2)
        self.hide_button_Left.clicked.connect(self.hide_show)
        self.hide_button_Right.clicked.connect(self.hide_show2)
        self.Start_Stop_Button_Right.clicked.connect(self.start_stop2)
        self.Start_Stop_Button_Left.clicked.connect(self.start_stop)
        self.Print_button_Left.clicked.connect(self.createPDF)
        self.Print_button_Right.clicked.connect(self.createPDF2)
        self.Snap_button_Left.clicked.connect(self.snap)
        self.Snap_button_Right.clicked.connect(self.snap2)
        self.MoveToGraph2_Button.clicked.connect(self.moveto_graph2)
        self.Rewind_button_Left.clicked.connect(self.rewind)
        self.Rewind_button_Right.clicked.connect(self.rewind2)
        self.ChangeColor_Button_Left.clicked.connect(self.open_color_selection)
        self.ChangeColor_Button_Right.clicked.connect(
            self.open_color_selection2)
        self.Link_Button.clicked.connect(self.link)
        self.MoveToGraph1_Button.clicked.connect(self.moveto_graph1)

        # self.horizontalScroller.valueChanged.connect(self.horzScrollBarChanged)
        self.horizontalScroller.valueChanged.connect(self.horizontalscroll)
        self.verticalSlider.valueChanged.connect(self.vertScrollBarChanged)
        self.horizontalScroller_2.valueChanged.connect(
            self.horizontalscroll2)
        self.verticalSlider_2.valueChanged.connect(self.vertScrollBarChanged_2)

        # to allow overlapping
        self.x_values_LGraph = []
        self.y_values_LGraph = []
        self.max_data_points = 0

        self.timer = None

        self.x_values_RGraph = []
        self.y_values_RGraph = []
        self.max_data_points2 = 0

        self.timer2 = None

        # self.selected_channel = None
        reference = []

        # label
        self.lineEdit.returnPressed.connect(self.update_channel_name)
        # widget
        self.lineEdit_2.returnPressed.connect(self.update_channel_name2)
        self.x_LGraph_To_Move = []
        self.y_LGraph_To_Move = []

        self.x_RGraph_To_Move = []
        self.y_RGraph_To_Move = []

        self.ComboBox_Left.currentIndexChanged.connect(self.Hidden_State)
        self.ComboBox_Right.currentIndexChanged.connect(self.Hidden_State2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ZoomIn_Button_Left.setText(_translate("MainWindow", "zoom in"))
        self.ZoomOut_Button_Left.setText(_translate("MainWindow", "zoom out"))
        self.Start_Stop_Button_Left.setText(
            _translate("MainWindow", "Start/Stop"))
        self.ChangeColor_Button_Left.setText(
            _translate("MainWindow", "Change Color"))
        self.Speed_Label_Left.setText(
            _translate("MainWindow", "Playback Speed"))
        self.hide_button_Left.setText(_translate("MainWindow", "Hide"))
        self.Snap_button_Left.setText(_translate("MainWindow", "Snap"))
        self.Label.setText(_translate("MainWindow", "Label:"))
        self.Browse_button_Left.setText(_translate("MainWindow", "Browse"))
        self.Rewind_button_Left.setText(_translate("MainWindow", "Rewind"))
        self.select_channel_label_Left.setText(
            _translate("MainWindow", "Select Channel:"))
        self.Print_button_Left.setText(_translate("MainWindow", "Print"))
        self.MoveToGraph2_Button.setText(_translate("MainWindow", "Move"))
        self.Link_Button.setText(_translate("MainWindow", "Link"))
        self.ZoomIn_Button_Right.setText(_translate("MainWindow", "zoom in"))
        self.ZoomOut_Button_Right.setText(_translate("MainWindow", "zoom out"))
        self.Start_Stop_Button_Right.setText(
            _translate("MainWindow", "Start/Stop"))
        self.ChangeColor_Button_Right.setText(
            _translate("MainWindow", "Change Color"))
        self.Speed_Label_Right.setText(
            _translate("MainWindow", "Playback Speed"))
        self.hide_button_Right.setText(_translate("MainWindow", "Hide"))
        self.Label_2.setText(_translate("MainWindow", "Label:"))
        self.Browse_button_Right.setText(_translate("MainWindow", "Browse"))
        self.select_channel_label_Right.setText(
            _translate("MainWindow", "Select Channel:"))
        self.Print_button_Right.setText(_translate("MainWindow", "Print"))
        self.MoveToGraph1_Button.setText(_translate("MainWindow", "Move"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionBrowse.setText(_translate("MainWindow", "Browse"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.Rewind_button_Right.setText(_translate("MainWindow", "Rewind"))
        self.Snap_button_Right.setText(_translate("MainWindow", "Snap"))

        self.plot_iteration = 0
        self.plot_iteration2 = 0

    def browsefiles(self):
        if self.moved2 == False:
            file_path, _ = QFileDialog.getOpenFileName(
                None, caption='Open File', directory='Task1DSP')
            if file_path:
                self.dataframe = None
                with open(file_path, 'r') as file:
                    try:
                        self.dataframe = pd.read_csv(file_path)
                        print(self.dataframe.iloc[:, 0])
                    except pd.errors.ParserError:
                        # Handle the case when the CSV file has no header
                        self.dataframe = pd.read_csv(file_path, header=None)
                        print(self.dataframe.iloc[:, 0])

                Xdataframe_LGraph = self.dataframe.iloc[:, 0].to_numpy()
                Ydataframe_LGraph = self.dataframe.iloc[:, 1].to_numpy()
                # Set self.Xdataframe_LGraph to the loaded data
                self.Xdataframe_LGraph = Xdataframe_LGraph
                # Set self.Ydataframe_LGraph to the loaded data
                self.Ydataframe_LGraph = Ydataframe_LGraph
                # Append new data to existing data arrays with a rolling buffer
                if len(self.x_values_LGraph) > 0:
                    max_data_points = max(
                        len(Xdataframe_LGraph), len(self.x_values_LGraph[0]))
                else:
                    max_data_points = len(Xdataframe_LGraph)

                self.x_LGraph_To_Move.append(Xdataframe_LGraph)
                self.y_LGraph_To_Move.append(Ydataframe_LGraph)
                self.x_values_LGraph.insert(0, Xdataframe_LGraph)
                self.y_values_LGraph.insert(0, Ydataframe_LGraph)

                # Trim the buffer to the maximum data points
                self.x_values_LGraph = self.x_values_LGraph[:max_data_points]
                self.y_values_LGraph = self.y_values_LGraph[:max_data_points]
                self.Xcoordinates = self.x_values_LGraph.copy()

                # Update the maximum data points
                self.max_data_points = max(
                    self.max_data_points, max_data_points)

                # If the timer is not running or timer is None, start it
                if self.timer is None or not self.timer.isActive():
                    self.setup_timer()

                self.x_range = [0, self.max_data_points]

                # selecting channel
                # Generate a channel name
                # Create a new channel name for this data file
                channel_name = f"Channel {len(self.channel_names)}"
                self.channel_names.append(channel_name)
                channel_color = random.randint(0, 255), random.randint(
                    0, 255), random.randint(0, 255)
                self.channel_colors[channel_name] = channel_color

                self.ComboBox_Left.addItem(channel_name)

                self.channels.append((channel_name, self.dataframe))
                self.hidden_data.append(False)
                self.moved_data.append(False)

                self.Speed_Label_Left.setText(f"Speed: 1x")

                # statistics = self.calculate_statistics(Ydataframe_LGraph)
                # self.statistics.append(statistics)
        else:
            current_index = self.ComboBox_Right.currentIndex()
            Xdataframe_RGraph = self.x_RGraph_To_Move[current_index]
            # Append new data to existing data arrays with a rolling buffer
            if len(self.x_values_LGraph) > 0:
                max_data_points = max(
                    len(Xdataframe_RGraph), len(self.x_values_LGraph[0]))
            else:
                max_data_points = len(Xdataframe_RGraph)
            self.x_values_LGraph.insert(0, Xdataframe_RGraph)

            self.y_values_LGraph.insert(
                0, self.y_RGraph_To_Move[current_index])

            # Trim the buffer to the maximum data points
            self.x_values_LGraph = self.x_values_LGraph[:max_data_points]
            self.y_values_LGraph = self.y_values_LGraph[:max_data_points]

            # Update the maximum data points
            self.max_data_points = max(
                self.max_data_points, max_data_points)

            # If the timer is not running or timer is None, start it
            if self.timer is None or not self.timer.isActive():
                self.setup_timer()
            self.hidden_data.append(False)

            self.x_range = [0, self.max_data_points]
            self.Speed_Label_Left.setText(f"Speed: 1x")
            # statistics = self.calculate_statistics(self.x_RGraph_To_Move[current_index])
            # self.statistics.append(statistics)

    def setup_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)  # Update plot every 50 milliseconds
        self.Left_Graph.setLimits(xMin=0, xMax=float('inf'))
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.plot_iteration = 0

    def update_plot_data(self, channel_index=None):

        if self.plot_iteration < self.max_data_points:
            self.Xplotted += 1
            x_range_end = self.plot_iteration  # Set it to the current iteration
            self.Left_Graph.setLimits(yMin=min(self.y_values_LGraph[0][:self.Xplotted]), yMax=max(
                self.y_values_LGraph[0][:self.Xplotted]))
            self.Left_Graph.setLimits(xMin=0, xMax=max(
                self.x_values_LGraph[0][:self.plot_iteration + 1]))
            # Clear the Left_Graph
            self.Left_Graph.clear()
            # Adjust the range as needed
            x_range_start = max(0, x_range_end - 100)

            # Plot all data arrays up to the current iteration
            for i in range(len(self.x_values_LGraph)):
                if i in range(len(self.channels)):
                    x = self.x_values_LGraph[i][:self.plot_iteration]
                    y = self.y_values_LGraph[i][:self.plot_iteration]
                    # Create a pen for the channel.
              # G # Get the color for the channel.
                    if i not in self.channel_colors:
                        # Generate a random color for the channel.
                        random_color = get_random_color()

                        # Store the random color for the channel.
                        self.channel_colors[i] = random_color

                    channel_color = self.channel_colors[i]

                    # Create a pen for the channel.
                    # pen = pg.mkPen(channel_color)

                    if channel_index is None or channel_index == i:
                        # Create a pen for the channel.
                        pen = pg.mkPen(channel_color)
                        if self.hidden_data[i] == False:
                            # print(f"Plotted iteration {self.plot_iteration}")
                            self.Left_Graph.plot(
                                x, y, pen=pen, name=self.channel_names[i])
                else:
                    break
             # if i in range(len(self.channels)):
                self.x_range = [x_range_start, x_range_end]
                self.Left_Graph.setXRange(*self.x_range)
                self.Left_Graph.setXRange(
                    self.x_values_LGraph[0][x_range_start], self.x_values_LGraph[0][x_range_end])

                self.plot_iteration += 1
        else:
            self.timer.stop()  # Stop the QTimer when finished

    def rewind(self):
        # Reset the plot iteration counters to 0
        self.plot_iteration = 0
       # self.plot_iteration2 = 0

        # Restart the timers to resume plotting
        if self.running:
            self.timer.start()

        # if self.running2:
        #     self.timer2.start()

    def rewind2(self):
        # Reset the plot iteration counters to 0
        # self.plot_iteration = 0
        self.plot_iteration2 = 0

        # Restart the timers to resume plotting
        if self.running2:
            self.timer2.start()

    def browsefiles2(self):
        if self.moved == False:
            file_path, _ = QFileDialog.getOpenFileName(
                None, caption='Open File', directory='Task1DSP')
            if file_path:
                self.dataframe2 = None
                with open(file_path, 'r') as file:
                    try:
                        self.dataframe2 = pd.read_csv(file_path)
                        print(self.dataframe2.iloc[:, 0])
                    except pd.errors.ParserError:
                        # Handle the case when the CSV file has no header
                        self.dataframe2 = pd.read_csv(file_path, header=None)
                        print(self.dataframe2.iloc[:, 0])

                Xdataframe_RGraph = self.dataframe2.iloc[:, 0].to_numpy()
                Ydataframe_RGraph = self.dataframe2.iloc[:, 1].to_numpy()
                # Set self.Xdataframe_LGraph to the loaded data
                self.Xdataframe_RGraph = Xdataframe_RGraph
                # Set self.Ydataframe_LGraph to the loaded data
                self.Ydataframe_RGraph = Ydataframe_RGraph
                # Append new data to existing data arrays with a rolling buffer
                if len(self.x_values_RGraph) > 0:
                    max_data_points2 = max(
                        len(Xdataframe_RGraph), len(self.x_values_RGraph[0]))
                else:
                    max_data_points2 = len(Xdataframe_RGraph)

                self.x_RGraph_To_Move.append(Xdataframe_RGraph)
                self.y_RGraph_To_Move.append(Ydataframe_RGraph)
                self.x_values_RGraph.insert(0, Xdataframe_RGraph)
                self.y_values_RGraph.insert(0, Ydataframe_RGraph)

                # Trim the buffer to the maximum data points
                self.x_values_RGraph = self.x_values_RGraph[:max_data_points2]
                self.y_values_RGraph = self.y_values_RGraph[:max_data_points2]

                # Update the maximum data points
                self.max_data_points2 = max(
                    self.max_data_points2, max_data_points2)

                # If the timer is not running or timer is None, start it
                if self.timer2 is None or not self.timer2.isActive():
                    self.setup_timer2()

                self.x_range2 = [0, self.max_data_points2]

                # selecting channel
                # Generate a channel name
                # Create a new channel name for this data file
                channel_name = f"Channel {len(self.channel_names2)}"
                self.channel_names2.append(channel_name)

                channel_color = random.randint(0, 255), random.randint(
                    0, 255), random.randint(0, 255)
                self.channel_colors2[channel_name] = channel_color
                # Add the channel name to the combo box
                self.ComboBox_Right.addItem(channel_name)

                # Store the data in your list (self.channels)
                self.channels2.append((channel_name, self.dataframe2))
                self.hidden_data2.append(False)
                self.moved_data2.append(False)
                self.Speed_Label_Right.setText(f"Speed: 1x")
                # Add the channel name to the combo box
                # self.ComboBox_Left.addItem(channel_name)
                # self.hidden_data.append(False)
                # self.ComboBox_Left.currentIndexChanged.connect(self.select_channel)
                # statistics = self.calculate_statistics(Xdataframe_RGraph)
                # self.statistics.append(statistics)
                # self.update_table()
        else:
            current_index = self.ComboBox_Left.currentIndex()
            Xdataframe_LGraph = self.x_LGraph_To_Move[current_index]
            # Append new data to existing data arrays with a rolling buffer
            if len(self.x_values_RGraph) > 0:
                max_data_points2 = max(
                    len(Xdataframe_LGraph), len(self.x_values_RGraph[0]))
            else:
                max_data_points2 = len(Xdataframe_LGraph)
            self.x_values_RGraph.insert(0, Xdataframe_LGraph)

            self.y_values_RGraph.insert(
                0, self.y_LGraph_To_Move[current_index])

            # Trim the buffer to the maximum data points
            self.x_values_RGraph = self.x_values_RGraph[:max_data_points2]
            self.y_values_RGraph = self.y_values_RGraph[:max_data_points2]

            # Update the maximum data points
            self.max_data_points2 = max(
                self.max_data_points2, max_data_points2)

            # If the timer is not running or timer is None, start it
            if self.timer2 is None or not self.timer2.isActive():
                self.setup_timer2()
            self.hidden_data2.append(False)

            self.x_range2 = [0, self.max_data_points2]
            self.Speed_Label_Right.setText(f"Speed: 1x")
            # statistics = self.calculate_statistics(self.x_LGraph_To_Move[current_index])
            # self.statistics.append(statistics)

    def setup_timer2(self):
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(100)  # Update plot every 50 milliseconds
        self.timer2.timeout.connect(self.update_plot_data2)
        self.timer2.start()

    def update_plot_data2(self, channel_index=None):
        if self.plot_iteration2 < self.max_data_points2:
            self.Xplotted2 += 1
            # Clear the Left_Graph
            self.Right_Graph.clear()
            x_range_end = self.plot_iteration2  # Set it to the current iteration
            # Adjust the range as needed
            x_range_start = max(0, x_range_end - 100)
            self.Right_Graph.setLimits(yMin=min(self.y_values_RGraph[0][:self.Xplotted2]), yMax=max(
                self.y_values_RGraph[0][:self.Xplotted2]))
            self.Right_Graph.setLimits(xMin=0, xMax=max(
                self.x_values_RGraph[0][:self.Xplotted2 + 1]))
            # Plot all data arrays up to the current iteration
            for i in range(len(self.x_values_RGraph)):
                x = self.x_values_RGraph[i][:self.plot_iteration2]
                y = self.y_values_RGraph[i][:self.plot_iteration2]
                if i not in self.channel_colors2:
                    # Generate a random color for the channel.
                    random_color = get_random_color()

                    # Store the random color for the channel.
                    self.channel_colors2[i] = random_color

                channel_color = self.channel_colors2[i]

                # Create a pen for the channel.
                # pen = pg.mkPen(channel_color)

                if channel_index is None or channel_index == i:
                    # Create a pen for the channel.
                    pen = pg.mkPen(channel_color)
                    if self.hidden_data2[i] == False:
                        self.Right_Graph.plot(
                            x, y, pen=pen, name=self.channel_names2[i])
            self.x_range = [x_range_start, x_range_end]
            self.Right_Graph.setXRange(*self.x_range)
            self.Right_Graph.setXRange(
                self.x_values_RGraph[0][x_range_start], self.x_values_RGraph[0][x_range_end])

            self.plot_iteration2 += 1
        else:
            self.timer2.stop()  # Stop the QTimer when finished

    def Hidden_State(self):
        selected_channel_index = self.ComboBox_Left.currentIndex()
        if self.hidden_data[selected_channel_index] == True:
            self.hide_button_Left.setText("Show")

        else:
            self.hide_button_Left.setText("Hide")

    def Hidden_State2(self):
        selected_channel_index = self.ComboBox_Right.currentIndex()
        if self.hidden_data2[selected_channel_index] == True:
            self.hide_button_Right.setText("Show")

        else:
            self.hide_button_Right.setText("Hide")

    def hide_show(self):
        selected_channel_index = self.ComboBox_Left.currentIndex()
        if self.hidden_data[selected_channel_index] == True:
            # Clear the plot (remove all items) to hide everything
            self.hide_button_Left.setText("Hide")
            self.hidden_data[selected_channel_index] = False
        else:
            # Re-plot only the data you want to show
            # if not self.hidden2_data1:
            self.hide_button_Left.setText("Show")
            self.hidden_data[selected_channel_index] = True

    def hide_show2(self):
        selected_channel_index = self.ComboBox_Right.currentIndex()
        if self.hidden_data2[selected_channel_index] == True:
            # Clear the plot (remove all items) to hide everything
            self.hide_button_Right.setText("Hide")
            self.hidden_data2[selected_channel_index] = False
        else:
            # Re-plot only the data you want to show
            # if not self.hidden2_data1:
            self.hide_button_Right.setText("Show")
            self.hidden_data2[selected_channel_index] = True

    # start_stop for widget
    def start_stop2(self):
        print("timer is not working")
        self.Right_Graph.setLimits(xMin=0, xMax=max(
            self.x_values_RGraph[0][:self.Xplotted2]))
        self.Right_Graph.setLimits(yMin=min(self.y_values_RGraph[0][:self.Xplotted2]), yMax=max(
            self.y_values_RGraph[0][:self.Xplotted2]))
        if self.running2:
            if self.graphs_linked:
                self.timer.stop()
                self.timer2.stop()
                # self.linked_timer.stop()
            else:
                self.timer2.stop()
        else:
            if self.graphs_linked:
                self.timer.start()
                self.timer2.start()
            else:
                self.timer2.start()
        self.running2 = not self.running2

    # start_stop for Left_Graph
    def start_stop(self):
        self.Left_Graph.setLimits(xMin=0, xMax=max(
            self.x_values_LGraph[0][:self.Xplotted]))
        self.Left_Graph.setLimits(yMin=min(self.y_values_LGraph[0][:self.Xplotted]), yMax=max(
            self.y_values_LGraph[0][:self.Xplotted]))
        if self.running:
            if self.graphs_linked:
                self.timer.stop()
                self.timer2.stop()
            else:
                self.timer.stop()
        else:
            if self.graphs_linked:
                self.timer.start()
                self.timer2.start()
            else:
                self.timer.start()
        self.running = not self.running

    def createPDF(self):
        folderpath = QFileDialog.getSaveFileName(
            None, str('Save File'), None, str("PDF Files(*.pdf"))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(70)
        pdf.cell(50, 40, "Signal Report", 0, 0, 'C')

        # Create a list to store the data statistics for all plotted data files
        all_data = []

        # Export images from the images array
        for image_path in self.images:
            pdf.image(image_path, 40, 50, 150, 100)
            # signal_label = self.ComboBox_Left.currentText()
            if self.images.index(image_path) < len(self.images) - 1:
                pdf.add_page()

        pdf.add_page()
        for i, data in enumerate(self.channels):
            x1 = data[1].iloc[:, 0].to_numpy()
            y1 = data[1].iloc[:, 1].to_numpy()

            mean = np.mean(y1)
            std_dev = np.std(y1)
            duration = len(y1)
            min_val = np.min(y1)
            max_val = np.max(y1)

            # Add the statistics to the list
            all_data.append(
                [self.ComboBox_Left.itemText(i), f'{mean:.2f}', f'{std_dev:.2f}', duration, f'{min_val:.2f}', f'{max_val:.2f}'])

            # Create a PDF table for each data file
            if i == 0:
                table_data = [['Signal Label', 'Mean', 'Std Dev',
                               'Duration', 'Min', 'Max']] + all_data
            else:
                table_data = all_data

            self.add_table_to_pdf(pdf, table_data)

        pdf.output(str(folderpath[0]))

    def add_table_to_pdf(self, pdf, data):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(30, 10, '', 0, 1)
        for row in data:
            for item in row:
                pdf.cell(35, 10, str(item), 1)
            pdf.ln()
        pdf.cell(40, 10, '', 0, 1)

    def snap(self):
        # Create a new image exporter
        exporter = pg.exporters.ImageExporter(self.Left_Graph.plotItem)
        image_path = f'snapshot_{len(self.images)}.png'
        exporter.export(image_path)
        # Append the image path to the images array
        self.images.append(image_path)

    def snap2(self):
        # Create a new image exporter
        exporter = pg.exporters.ImageExporter(self.Right_Graph.plotItem)
        image_path = f'snapshot_{len(self.images2)}.png'
        exporter.export(image_path)

        # Append the image path to the images array
        self.images2.append(image_path)

    def createPDF2(self):
        folderpath = QFileDialog.getSaveFileName(
            None, str('Save File'), None, str("PDF Files(*.pdf"))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(70)
        pdf.cell(50, 40, "Signal Report", 0, 0, 'C')

        # Create a list to store the data statistics for all plotted data files
        all_data = []

        # Export images from the images array
        for image_path in self.images2:
            pdf.image(image_path, 40, 50, 150, 100)
            # signal_label = self.ComboBox_Left.currentText()
            if self.images2.index(image_path) < len(self.images2) - 1:
                pdf.add_page()

        pdf.add_page()
        for i, data in enumerate(self.channels2):
            x2 = data[1].iloc[:, 0].to_numpy()
            y2 = data[1].iloc[:, 1].to_numpy()

            mean = np.mean(y2)
            std_dev = np.std(y2)
            duration = len(y2)
            min_val = np.min(y2)
            max_val = np.max(y2)

            # Add the statistics to the list
            all_data.append(
                [self.ComboBox_Right.itemText(i), f'{mean:.2f}', f'{std_dev:.2f}', duration, min_val, max_val])

            # Create a PDF table for each data file
            if i == 0:
                table_data = [['Signal Label', 'Mean', 'Std Dev',
                               'Duration', 'Min', 'Max']] + all_data
            else:
                table_data = all_data

            self.add_table_to_pdf(pdf, table_data)

        pdf.output(str(folderpath[0]))

    def moveto_graph2(self):
        self.moved = True
        selected_channel_index = self.ComboBox_Left.currentIndex()
        # Get the selected channel index in the combo box.
        selected_channel_index = self.ComboBox_Left.currentIndex()

    # Get the channel name, color, dataframe, and hidden state for the selected channel.
        channel_name = self.channel_names[selected_channel_index]
        # channel_color = self.channel_colors[channel_name]
        dataframe = self.channels[selected_channel_index][1]
    # Remove the selected channel from the original widget.

        self.channels.pop(selected_channel_index)
        self.channel_names.pop(selected_channel_index)

        self.hidden_data.pop(selected_channel_index)
        channel_index = self.ComboBox_Left.findText(channel_name)
        if channel_index >= 0:
            self.ComboBox_Left.removeItem(channel_index)
    # Add the selected channel to the other widget.
        self.channels2.append((channel_name, dataframe))
        self.channel_names2.append(channel_name)
        self.hidden_data2.append(False)

    # Update the combo box.
        self.ComboBox_Right.addItem(channel_name)
        self.browsefiles2()
        self.moved = False

    def moveto_graph1(self):
        self.moved2 = True
        selected_channel_index = self.ComboBox_Right.currentIndex()

    # Get the channel name, color, dataframe, and hidden state for the selected channel.
        channel_name = self.channel_names2[selected_channel_index]

        dataframe = self.channels2[selected_channel_index][1]
    # Remove the selected channel from the original widget.

        self.channels2.pop(selected_channel_index)
        self.channel_names2.pop(selected_channel_index)

        self.hidden_data2.pop(selected_channel_index)
        channel_index = self.ComboBox_Right.findText(channel_name)
        if channel_index >= 0:
            self.ComboBox_Right.removeItem(channel_index)
    # Add the selected channel to the other widget.

        self.channels.append((channel_name, dataframe))
        self.channel_names.append(channel_name)
        self.hidden_data.append(False)

    # Update the combo box.
        self.ComboBox_Left.addItem(channel_name)
        self.browsefiles()
        self.moved2 = False

    def zoom_in(self):
        current_range = self.Left_Graph.viewRange()
        self.Left_Graph.setXRange(
            current_range[0][0] * 0.9, current_range[0][1] * 0.9, padding=0)
        self.Left_Graph.setYRange(
            current_range[1][0] * 0.9, current_range[1][1] * 0.9, padding=0)

    def zoom_out(self):
        current_range = self.Left_Graph.viewRange()
        self.Left_Graph.setXRange(
            current_range[0][0] * 1.1, current_range[0][1] * 1.1, padding=0)
        self.Left_Graph.setYRange(
            current_range[1][0] * 1.1, current_range[1][1] * 1.1, padding=0)

    def open_color_selection(self):
        color_dialog = ColorSelectionDialog(MainWindow)
        if color_dialog.exec_() != QDialog.Accepted:
            selected_color = color_dialog.color
            selected_channel_index = self.ComboBox_Left.currentIndex()
            self.change_color(selected_channel_index, selected_color)

    def change_color(self, channel_index, color):
        self.channel_colors[channel_index] = color

    def open_color_selection2(self):
        color_dialog = ColorSelectionDialog2(MainWindow)
        print("class 3ada")
       # color_dialog.color_selected.connect(self.change_color_dialog)
        if color_dialog.exec_() != QDialog.Accepted:
            print("if condition done")
            selected_color = color_dialog.color2
            selected_channel_index = self.ComboBox_Right.currentIndex()
            self.change_color2(selected_channel_index, selected_color)
            print("call change color")

    def change_color2(self, channel_index, color):
        self.channel_colors2[channel_index] = color

    def update_Speed_Label_Left(self, value):
        self.Speed_Label_Left.setText(f"Speed: {value}x")
        self.update_graph_speed(value)

    def update_graph_speed(self, speed, timer=None):
        # Calculate the timer interval based on the chosen speed
        if speed == 0:
            interval = 1000

        elif speed == 1:
            interval = 100
            self.timer.setInterval(interval)
        else:
            interval = int(1000 / speed)   # In milliseconds
            self.timer.setInterval(interval)

    def update_Speed_Label_Right(self, value):
        self.Speed_Label_Right.setText(f"Speed: {value}x")
        self.update_graph_speed_2(value)

    def update_graph_speed_2(self, speed, timer=None):
        # Calculate the timer interval based on the chosen speed
        if speed == 0:
            interval = 1000

        elif speed == 1:
            interval = 100
            self.timer2.setInterval(interval)
        else:
            interval = int(1000 / speed)   # In milliseconds
            self.timer2.setInterval(interval)

    def link(self):
        if self.graphs_linked:
            # Unlink the graphs
            self.Left_Graph.setXLink(None)
            self.Right_Graph.setYLink(None)
            self.graphs_linked = False
            self.Link_Button.setText("Link")
        else:
            self.Left_Graph.setXLink(self.Right_Graph)
            self.Right_Graph.setYLink(self.Left_Graph)
            # Link the graphs
            self.graphs_linked = True
            self.Link_Button.setText("Unlink")
            # Synchronize all buttons and graphs
            self.rewind()
            self.rewind2()

    def zoom_in2(self):
        current_range = self.Right_Graph.viewRange()
        self.Right_Graph.setXRange(
            current_range[0][0] * 0.9, current_range[0][1] * 0.9, padding=0)
        self.Right_Graph.setYRange(
            current_range[1][0] * 0.9, current_range[1][1] * 0.9, padding=0)

    def zoom_out2(self):
        current_range = self.Right_Graph.viewRange()
        self.Right_Graph.setXRange(
            current_range[0][0] * 1.1, current_range[0][1] * 1.1, padding=0)
        self.Right_Graph.setYRange(
            current_range[1][0] * 1.1, current_range[1][1] * 1.1, padding=0)

    def update_channel_name(self):
        # Get the current text from the QLineEdit
        new_name = self.lineEdit.text()

        # Get the current index of the selected item in the combo box
        selected_index = self.ComboBox_Left.currentIndex()

        # Ensure that the selected index is within a valid range
        if 0 <= selected_index < len(self.channel_names):
            # Update the name in the channel_names list
            self.channel_names[selected_index] = new_name

            # Update the combo box item with the new name
            self.ComboBox_Left.setItemText(selected_index, new_name)

    def update_channel_name2(self):
        # Get the current text from the QLineEdit
        new_name = self.lineEdit_2.text()

        # Get the current index of the selected item in the combo box
        selected_index = self.ComboBox_Right.currentIndex()

        # Ensure that the selected index is within a valid range
        if 0 <= selected_index < len(self.channel_names2):
            # Update the name in the channel_names list
            self.channel_names2[selected_index] = new_name

            # Update the combo box item with the new name
            self.ComboBox_Right.setItemText(selected_index, new_name)

    # Scroll
    def horizontalscroll(self, value):
        if value < 1:
            self.Left_Graph.getViewBox().setXRange(0, value)
        else:
            self.Left_Graph.getViewBox().setXRange(value - 1, value)

    def horizontalscroll2(self, value):
        if value < 1:
            self.Right_Graph.getViewBox().setXRange(0, value)
        else:
            self.Right_Graph.getViewBox().setXRange(value - 1, value)

    def vertScrollBarChanged(self, value):
        # self.Left_Graph.plotItem.getViewBox().setYRange(-value / 10.0, -value / 10.0 + self.Left_Graph.plotItem.viewRange()[1][1] - self.Left_Graph.plotItem.viewRange()[0][0])
        self.Left_Graph.setYRange(value / 10.0, value / 10.0 + self.Left_Graph.plotItem.viewRange()[
            1][0] - self.Left_Graph.plotItem.viewRange()[0][0])

    def vertScrollBarChanged_2(self, value):
        # self.Left_Graph.plotItem.getViewBox().setYRange(-value / 10.0, -value / 10.0 + self.Left_Graph.plotItem.viewRange()[1][1] - self.Left_Graph.plotItem.viewRange()[0][0])
        self.Right_Graph.setYRange(value / 10.0, value / 10.0 + self.Right_Graph.plotItem.viewRange()[
            1][0] - self.Right_Graph.plotItem.viewRange()[0][0])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
