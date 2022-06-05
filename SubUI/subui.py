from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    # subwindow of sutter
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.setEnabled(True)
        Dialog.resize(445, 370)
        Dialog.setFocusPolicy(QtCore.Qt.NoFocus)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.Res = QtWidgets.QLabel(Dialog)
        self.Res.setGeometry(QtCore.QRect(70, 50, 101, 16))
        self.Res.setObjectName("Res")
        self.Velocity = QtWidgets.QLabel(Dialog)
        self.Velocity.setGeometry(QtCore.QRect(70, 100, 101, 16))
        self.Velocity.setObjectName("Velocity")
        self.velocity = QtWidgets.QSpinBox(Dialog)
        self.velocity.setEnabled(True)
        self.velocity.setGeometry(QtCore.QRect(160, 100, 101, 21))
        self.velocity.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.velocity.setWrapping(False)
        self.velocity.setFrame(True)
        self.velocity.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.velocity.setSuffix("")
        self.velocity.setMaximum(3000)
        self.velocity.setProperty("value", 200)
        self.velocity.setObjectName("velocity")
        self.unit = QtWidgets.QLabel(Dialog)
        self.unit.setGeometry(QtCore.QRect(290, 100, 91, 16))
        self.unit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.unit.setObjectName("unit")
        self.ResH = QtWidgets.QCheckBox(Dialog)
        self.ResH.setGeometry(QtCore.QRect(180, 50, 91, 19))
        self.ResH.setObjectName("ResH")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 310, 193, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 190, 381, 91))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 72, 15))
        self.label_2.setObjectName("label_2")
        self.stepSize = QtWidgets.QDoubleSpinBox(Dialog)
        self.stepSize.setGeometry(QtCore.QRect(160, 150, 101, 22))
        self.stepSize.setMaximum(10000.0)
        self.stepSize.setSingleStep(0.04)
        self.stepSize.setObjectName("stepSize")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(290, 150, 111, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 210, 51, 51))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("icons/191-Attention.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sutter MP285"))
        self.Res.setText(_translate("Dialog", "Resolution:"))
        self.Velocity.setText(_translate("Dialog", "Velocity:"))
        self.unit.setText(_translate("Dialog", "micron/s"))
        self.ResH.setText(_translate("Dialog", "High"))
        self.label.setText(_translate("Dialog", "High resolution:\n"
"Step size should be multiples of 0.04\n"
"Low resolution:\n"
"Step size should be multiples of 0.2 "))
        self.label_2.setText(_translate("Dialog", "Step size:"))
        self.label_3.setText(_translate("Dialog", "microns/step"))

class Ui_Dialog2(object):
    # subwindow of prior
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
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.tabWidget.setPalette(palette)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setAutoFillBackground(False)
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
        self.stepSizeX.setGeometry(QtCore.QRect(100, 80, 121, 22))
        self.stepSizeX.setMaximum(1000)
        self.stepSizeX.setObjectName("stepSizeX")
        self.label_12 = QtWidgets.QLabel(self.default_param)
        self.label_12.setGeometry(QtCore.QRect(230, 80, 211, 20))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.default_param)
        self.label_13.setGeometry(QtCore.QRect(30, 120, 91, 16))
        self.label_13.setObjectName("label_13")
        self.stepSizeY = QtWidgets.QSpinBox(self.default_param)
        self.stepSizeY.setGeometry(QtCore.QRect(100, 120, 121, 22))
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
        self.label_14.setGeometry(QtCore.QRect(230, 120, 211, 20))
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
        self.Pattern = QtWidgets.QWidget()
        self.Pattern.setAutoFillBackground(True)
        self.Pattern.setObjectName("Pattern")
        self.label_10 = QtWidgets.QLabel(self.Pattern)
        self.label_10.setGeometry(QtCore.QRect(130, 30, 119, 31))
        self.label_10.setObjectName("label_10")
        self.label_25 = QtWidgets.QLabel(self.Pattern)
        self.label_25.setGeometry(QtCore.QRect(130, 80, 81, 21))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.Pattern)
        self.label_26.setGeometry(QtCore.QRect(130, 120, 81, 31))
        self.label_26.setObjectName("label_26")
        self.label_29 = QtWidgets.QLabel(self.Pattern)
        self.label_29.setGeometry(QtCore.QRect(90, 170, 119, 41))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.Pattern)
        self.label_30.setGeometry(QtCore.QRect(140, 220, 71, 41))
        self.label_30.setObjectName("label_30")
        self.xFields = QtWidgets.QSpinBox(self.Pattern)
        self.xFields.setGeometry(QtCore.QRect(220, 80, 46, 22))
        self.xFields.setObjectName("xFields")
        self.yFields = QtWidgets.QSpinBox(self.Pattern)
        self.yFields.setGeometry(QtCore.QRect(220, 130, 46, 22))
        self.yFields.setObjectName("yFields")
        self.repeat = QtWidgets.QSpinBox(self.Pattern)
        self.repeat.setGeometry(QtCore.QRect(220, 230, 46, 22))
        self.repeat.setMaximum(10)
        self.repeat.setObjectName("repeat")
        self.timeInter = QtWidgets.QDoubleSpinBox(self.Pattern)
        self.timeInter.setGeometry(QtCore.QRect(220, 180, 70, 22))
        self.timeInter.setDecimals(1)
        self.timeInter.setMinimum(0.5)
        self.timeInter.setMaximum(10.0)
        self.timeInter.setSingleStep(0.1)
        self.timeInter.setObjectName("timeInter")
        self.tabWidget.addTab(self.Pattern, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Prior"))
        self.label_11.setText(_translate("Dialog", "X Step:"))
        self.stepSizeX.setSuffix(_translate("Dialog", "microns"))
        self.label_12.setText(_translate("Dialog", "(Including scan step size)"))
        self.label_13.setText(_translate("Dialog", "Y Step:"))
        self.stepSizeY.setSuffix(_translate("Dialog", "microns"))
        self.label_15.setText(_translate("Dialog", "Correction:"))
        self.correction4P.setText(_translate("Dialog", "4-Point Stage Correction"))
        self.label_16.setText(_translate("Dialog", "BackLash:"))
        self.HBLenable.setText(_translate("Dialog", "Stage Host Back Lash Enable"))
        self.label_17.setText(_translate("Dialog", "Stage Host Back Lash Distance:"))
        self.label_18.setText(_translate("Dialog", "microsteps"))
        self.label_14.setText(_translate("Dialog", "(Including scan step size)"))
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
        self.label_10.setText(_translate("Dialog", "Type:Snake"))
        self.label_25.setText(_translate("Dialog", "X Fields:"))
        self.label_26.setText(_translate("Dialog", "Y Fields:"))
        self.label_29.setText(_translate("Dialog", "Time interval:"))
        self.label_30.setText(_translate("Dialog", "Repeats:"))
        self.timeInter.setSuffix(_translate("Dialog", "s"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Pattern), _translate("Dialog", "Pattern"))

class Ui_Dialog3(object):
    # subwinow of Basler
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(698, 273)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 220, 391, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 50, 201, 16))
        self.label_2.setObjectName("label_2")
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_2.setGeometry(QtCore.QRect(350, 50, 101, 22))
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(600)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 90, 641, 111))
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Camera "))
        self.label_2.setText(_translate("Dialog", "Time of auto record:"))
        self.spinBox_2.setSuffix(_translate("Dialog", "s"))
        self.label_3.setText(_translate("Dialog", "Information and parameter settings of the camera can be found in \'NodeMap.pfs\'\n"
"And all the setting will be initialized when cam opening.\n"
"Therefore,if you want to change the parameters of camera,\n"
"please firstly change the settings in *.pfs document\n"
"and then generated a new file"))

class Ui_Dialog4(object):
    # Subwindow of devices
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 279)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(260, 230, 121, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 171, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(220, 60, 201, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(210, 90, 201, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(220, 120, 171, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(90, 150, 51, 51))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("icons/warning_fill.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(170, 140, 441, 71))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Devices connection"))
        self.label.setText(_translate("Dialog", "Defalut connection:"))
        self.label_2.setText(_translate("Dialog", "Basler camera:GigE"))
        self.label_3.setText(_translate("Dialog", "Prior ProScanIII:COM3"))
        self.label_4.setText(_translate("Dialog", "Sutter MP285A:COM4"))
        self.label_6.setText(_translate("Dialog", "Wrong COM port numberw won\'t impact the initialization\n"
"Please check the power or the connecting cable \n"
"if you fail to connnect the decives "))

