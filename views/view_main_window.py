# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 693)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_5 = QFrame(self.centralwidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(self.frame_5)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.cbSelectCam = QComboBox(self.frame)
        self.cbSelectCam.setObjectName(u"cbSelectCam")

        self.verticalLayout.addWidget(self.cbSelectCam)

        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnConnect = QPushButton(self.frame_7)
        self.btnConnect.setObjectName(u"btnConnect")

        self.horizontalLayout.addWidget(self.btnConnect)

        self.btnScan = QPushButton(self.frame_7)
        self.btnScan.setObjectName(u"btnScan")

        self.horizontalLayout.addWidget(self.btnScan)

        self.toolButton_2 = QToolButton(self.frame_7)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout.addWidget(self.toolButton_2)


        self.verticalLayout.addWidget(self.frame_7)


        self.horizontalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_5)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.cbSelectInputFilter = QComboBox(self.frame_2)
        self.cbSelectInputFilter.setObjectName(u"cbSelectInputFilter")

        self.verticalLayout_2.addWidget(self.cbSelectInputFilter)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.cbSelectOuputFilter = QComboBox(self.frame_2)
        self.cbSelectOuputFilter.setObjectName(u"cbSelectOuputFilter")

        self.verticalLayout_2.addWidget(self.cbSelectOuputFilter)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.cbSelectModel = QComboBox(self.frame_3)
        self.cbSelectModel.setObjectName(u"cbSelectModel")

        self.verticalLayout_3.addWidget(self.cbSelectModel)

        self.frame_10 = QFrame(self.frame_3)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.enableCv = QPushButton(self.frame_10)
        self.enableCv.setObjectName(u"enableCv")

        self.horizontalLayout_5.addWidget(self.enableCv)

        self.toolButton_4 = QToolButton(self.frame_10)
        self.toolButton_4.setObjectName(u"toolButton_4")

        self.horizontalLayout_5.addWidget(self.toolButton_4)


        self.verticalLayout_3.addWidget(self.frame_10)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_5)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.comboBox_4 = QComboBox(self.frame_4)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.verticalLayout_4.addWidget(self.comboBox_4)

        self.frame_9 = QFrame(self.frame_4)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_3 = QPushButton(self.frame_9)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_4.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_9)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_4.addWidget(self.pushButton_4)

        self.toolButton_3 = QToolButton(self.frame_9)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout_4.addWidget(self.toolButton_3)


        self.verticalLayout_4.addWidget(self.frame_9)


        self.horizontalLayout_2.addWidget(self.frame_4)


        self.verticalLayout_5.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.parameters = QTabWidget(self.frame_6)
        self.parameters.setObjectName(u"parameters")
        self.parameters.setMaximumSize(QSize(1000, 1000))
        self.camTab = QWidget()
        self.camTab.setObjectName(u"camTab")
        self.parameters.addTab(self.camTab, "")
        self.filterTab = QWidget()
        self.filterTab.setObjectName(u"filterTab")
        self.parameters.addTab(self.filterTab, "")

        self.gridLayout.addWidget(self.parameters, 2, 0, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")

        self.gridLayout.addLayout(self.verticalLayout_8, 3, 0, 1, 1)

        self.cam = QLabel(self.frame_6)
        self.cam.setObjectName(u"cam")
        self.cam.setMaximumSize(QSize(1000, 1000))

        self.gridLayout.addWidget(self.cam, 1, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName(u"label_6")
        font = QFont()
        font.setFamilies([u"DejaVu Sans Mono"])
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setMouseTracking(False)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.frame_6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.parameters.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select CAM", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.btnScan.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Input Filter", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Output Filter", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Load CV Model", None))
        self.enableCv.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.toolButton_4.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Select Communication", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.parameters.setTabText(self.parameters.indexOf(self.camTab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.parameters.setTabText(self.parameters.indexOf(self.filterTab), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.cam.setText(QCoreApplication.translate("MainWindow", u"CAM", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"LABORATORIO DE ROBOTICA UTN FRA", None))
    # retranslateUi

