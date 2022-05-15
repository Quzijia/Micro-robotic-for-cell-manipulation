# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uprior.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(459, 538)
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(120, 490, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 461, 481))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.tabWidget.setPalette(palette)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.default_param = QtWidgets.QWidget()
        self.default_param.setAutoFillBackground(True)
        self.default_param.setObjectName("default_param")
        self.label_11 = QtWidgets.QLabel(self.default_param)
        self.label_11.setGeometry(QtCore.QRect(30, 80, 91, 16))
        self.label_11.setObjectName("label_11")
        self.stepSizeX = QtWidgets.QSpinBox(self.default_param)
        self.stepSizeX.setGeometry(QtCore.QRect(130, 80, 71, 22))
        self.stepSizeX.setMaximum(1000)
        self.stepSizeX.setObjectName("stepSizeX")
        self.label_12 = QtWidgets.QLabel(self.default_param)
        self.label_12.setGeometry(QtCore.QRect(220, 80, 61, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.default_param)
        self.label_13.setGeometry(QtCore.QRect(30, 120, 91, 16))
        self.label_13.setObjectName("label_13")
        self.stepSizeY = QtWidgets.QSpinBox(self.default_param)
        self.stepSizeY.setGeometry(QtCore.QRect(130, 120, 71, 22))
        self.stepSizeY.setMaximum(1000)
        self.stepSizeY.setObjectName("stepSizeY")
        self.label_15 = QtWidgets.QLabel(self.default_param)
        self.label_15.setGeometry(QtCore.QRect(30, 160, 101, 16))
        self.label_15.setObjectName("label_15")
        self.correction4P = QtWidgets.QCheckBox(self.default_param)
        self.correction4P.setGeometry(QtCore.QRect(30, 200, 281, 19))
        self.correction4P.setObjectName("correction4P")
        self.label_16 = QtWidgets.QLabel(self.default_param)
        self.label_16.setGeometry(QtCore.QRect(30, 240, 72, 15))
        self.label_16.setObjectName("label_16")
        self.HBLenable = QtWidgets.QCheckBox(self.default_param)
        self.HBLenable.setGeometry(QtCore.QRect(30, 280, 261, 19))
        self.HBLenable.setObjectName("HBLenable")
        self.label_17 = QtWidgets.QLabel(self.default_param)
        self.label_17.setGeometry(QtCore.QRect(30, 310, 251, 20))
        self.label_17.setObjectName("label_17")
        self.HBLD = QtWidgets.QSpinBox(self.default_param)
        self.HBLD.setGeometry(QtCore.QRect(280, 310, 71, 22))
        self.HBLD.setMaximum(250)
        self.HBLD.setObjectName("HBLD")
        self.label_18 = QtWidgets.QLabel(self.default_param)
        self.label_18.setGeometry(QtCore.QRect(360, 310, 81, 16))
        self.label_18.setObjectName("label_18")
        self.label_14 = QtWidgets.QLabel(self.default_param)
        self.label_14.setGeometry(QtCore.QRect(220, 120, 61, 16))
        self.label_14.setObjectName("label_14")
        self.tabWidget.addTab(self.default_param, "")
        self.stage = QtWidgets.QWidget()
        self.stage.setAutoFillBackground(True)
        self.stage.setObjectName("stage")
        self.label_2 = QtWidgets.QLabel(self.stage)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 72, 15))
        self.label_2.setObjectName("label_2")
        self.speed = QtWidgets.QSpinBox(self.stage)
        self.speed.setGeometry(QtCore.QRect(90, 100, 91, 22))
        self.speed.setMaximum(10000)
        self.speed.setObjectName("speed")
        self.label_3 = QtWidgets.QLabel(self.stage)
        self.label_3.setGeometry(QtCore.QRect(190, 100, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.stage)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 101, 16))
        self.label_4.setObjectName("label_4")
        self.acceleteation = QtWidgets.QSpinBox(self.stage)
        self.acceleteation.setGeometry(QtCore.QRect(140, 150, 91, 22))
        self.acceleteation.setMaximum(28560)
        self.acceleteation.setObjectName("acceleteation")
        self.label_5 = QtWidgets.QLabel(self.stage)
        self.label_5.setGeometry(QtCore.QRect(250, 150, 101, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.stage)
        self.label_6.setGeometry(QtCore.QRect(30, 200, 101, 16))
        self.label_6.setObjectName("label_6")
        self.curve = QtWidgets.QSpinBox(self.stage)
        self.curve.setGeometry(QtCore.QRect(90, 200, 91, 22))
        self.curve.setMaximum(1000)
        self.curve.setObjectName("curve")
        self.label_7 = QtWidgets.QLabel(self.stage)
        self.label_7.setGeometry(QtCore.QRect(200, 200, 121, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.stage)
        self.label_8.setGeometry(QtCore.QRect(50, 310, 51, 51))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("icons/warning_fill.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.stage)
        self.label_9.setGeometry(QtCore.QRect(110, 300, 451, 61))
        self.label_9.setObjectName("label_9")
        self.tabWidget.addTab(self.stage, "")
        self.joystick = QtWidgets.QWidget()
        self.joystick.setAutoFillBackground(True)
        self.joystick.setObjectName("joystick")
        self.label = QtWidgets.QLabel(self.joystick)
        self.label.setGeometry(QtCore.QRect(30, 70, 181, 16))
        self.label.setObjectName("label")
        self.joySpeed = QtWidgets.QSpinBox(self.joystick)
        self.joySpeed.setGeometry(QtCore.QRect(150, 70, 91, 22))
        self.joySpeed.setPrefix("")
        self.joySpeed.setMaximum(100)
        self.joySpeed.setObjectName("joySpeed")
        self.joyXrever = QtWidgets.QCheckBox(self.joystick)
        self.joyXrever.setGeometry(QtCore.QRect(30, 110, 181, 19))
        self.joyXrever.setObjectName("joyXrever")
        self.joyYrever = QtWidgets.QCheckBox(self.joystick)
        self.joyYrever.setGeometry(QtCore.QRect(30, 150, 181, 19))
        self.joyYrever.setObjectName("joyYrever")
        self.HostXrever = QtWidgets.QCheckBox(self.joystick)
        self.HostXrever.setGeometry(QtCore.QRect(30, 190, 171, 19))
        self.HostXrever.setObjectName("HostXrever")
        self.HostYrever = QtWidgets.QCheckBox(self.joystick)
        self.HostYrever.setGeometry(QtCore.QRect(30, 230, 141, 19))
        self.HostYrever.setObjectName("HostYrever")
        self.joystickEnable = QtWidgets.QCheckBox(self.joystick)
        self.joystickEnable.setGeometry(QtCore.QRect(30, 270, 161, 19))
        self.joystickEnable.setObjectName("joystickEnable")
        self.tabWidget.addTab(self.joystick, "")
        self.others = QtWidgets.QWidget()
        self.others.setAutoFillBackground(True)
        self.others.setObjectName("others")
        self.label_19 = QtWidgets.QLabel(self.others)
        self.label_19.setGeometry(QtCore.QRect(40, 20, 101, 16))
        self.label_19.setObjectName("label_19")
        self.Description = QtWidgets.QLineEdit(self.others)
        self.Description.setGeometry(QtCore.QRect(40, 50, 113, 21))
        self.Description.setObjectName("Description")
        self.label_20 = QtWidgets.QLabel(self.others)
        self.label_20.setGeometry(QtCore.QRect(170, 50, 101, 16))
        self.label_20.setObjectName("label_20")
        self.Xtravel = QtWidgets.QLineEdit(self.others)
        self.Xtravel.setGeometry(QtCore.QRect(40, 90, 113, 21))
        self.Xtravel.setObjectName("Xtravel")
        self.label_21 = QtWidgets.QLabel(self.others)
        self.label_21.setGeometry(QtCore.QRect(170, 90, 101, 16))
        self.label_21.setObjectName("label_21")
        self.Ytravel = QtWidgets.QLineEdit(self.others)
        self.Ytravel.setGeometry(QtCore.QRect(40, 130, 113, 21))
        self.Ytravel.setObjectName("Ytravel")
        self.label_22 = QtWidgets.QLabel(self.others)
        self.label_22.setGeometry(QtCore.QRect(170, 130, 101, 16))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.others)
        self.label_23.setGeometry(QtCore.QRect(170, 170, 151, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.others)
        self.label_24.setGeometry(QtCore.QRect(40, 250, 101, 16))
        self.label_24.setObjectName("label_24")
        self.encoderEnable = QtWidgets.QCheckBox(self.others)
        self.encoderEnable.setGeometry(QtCore.QRect(40, 280, 201, 19))
        self.encoderEnable.setObjectName("encoderEnable")
        self.microStep = QtWidgets.QSpinBox(self.others)
        self.microStep.setGeometry(QtCore.QRect(40, 170, 111, 22))
        self.microStep.setMaximum(250)
        self.microStep.setObjectName("microStep")
        self.tabWidget.addTab(self.others, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Prior"))
        self.label_11.setText(_translate("Dialog", "X Step Size"))
        self.label_12.setText(_translate("Dialog", "microns"))
        self.label_13.setText(_translate("Dialog", "Y Step Size"))
        self.label_15.setText(_translate("Dialog", "Correction:"))
        self.correction4P.setText(_translate("Dialog", "4-Point Stage Correction"))
        self.label_16.setText(_translate("Dialog", "BackLash:"))
        self.HBLenable.setText(_translate("Dialog", "Stage Host Back Lash Enable"))
        self.label_17.setText(_translate("Dialog", "Stage Host Back Lash Distance:"))
        self.label_18.setText(_translate("Dialog", "microsteps"))
        self.label_14.setText(_translate("Dialog", "microns"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.default_param), _translate("Dialog", "Default"))
        self.label_2.setText(_translate("Dialog", "Speed:"))
        self.label_3.setText(_translate("Dialog", "microns/s"))
        self.label_4.setText(_translate("Dialog", "Acceleration:"))
        self.label_5.setText(_translate("Dialog", "microns/s/s"))
        self.label_6.setText(_translate("Dialog", "Curve:"))
        self.label_7.setText(_translate("Dialog", "microns/s/s/s"))
        self.label_9.setText(_translate("Dialog", "Stage may stop working \n"
"under certain setup conditions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stage), _translate("Dialog", "Stage"))
        self.label.setText(_translate("Dialog", "Joystick Speed"))
        self.joySpeed.setSuffix(_translate("Dialog", "%"))
        self.joyXrever.setText(_translate("Dialog", "Joy X reverse"))
        self.joyYrever.setText(_translate("Dialog", "Joy Y reverse"))
        self.HostXrever.setText(_translate("Dialog", "Host X reverse"))
        self.HostYrever.setText(_translate("Dialog", "Host Y reverse"))
        self.joystickEnable.setText(_translate("Dialog", "Joystick enable"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.joystick), _translate("Dialog", "Joystick"))
        self.label_19.setText(_translate("Dialog", "Stage Params"))
        self.Description.setText(_translate("Dialog", "USER"))
        self.label_20.setText(_translate("Dialog", "Description"))
        self.Xtravel.setText(_translate("Dialog", "114"))
        self.label_21.setText(_translate("Dialog", "X Travel(mm)"))
        self.Ytravel.setText(_translate("Dialog", "75"))
        self.label_22.setText(_translate("Dialog", "Y Travel(mm)"))
        self.label_23.setText(_translate("Dialog", "Micro Steps/micron"))
        self.label_24.setText(_translate("Dialog", "Encoder"))
        self.encoderEnable.setText(_translate("Dialog", "Stage Encoder Enable"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.others), _translate("Dialog", "Others"))
