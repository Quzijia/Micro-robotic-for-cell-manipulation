import glob
import queue
import re
import sys
import threading
import time
from pathlib import Path

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from imageio import get_writer
# Used to encode video

import pypylon.pylon as pylon
from Prior import Prior
from Sutter import MP285
from UIwindow import Ui_MainWindow
from InitParamas import paramas
from Subwindows import BaslerWindow, DevicesWindow, PriorWindow, SutterWindow, Worksignal, Runnable


class Window(QMainWindow):
    def __init__(self, frame_queue):
        super(Window, self).__init__()
        self.pos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signalslots()
        # self.setMouseTracking(True)
        self.connectCam()
        self.connectController()
        self.connectSutter()
        self.frame_queue = frame_queue
        self.is_running = False
        self.initParams()

    def initParams(self):
        self.FlagP, self.FlagS, self.FlagImg, self.FlagP, self.priorStepSizeX, self.priorStepSizeY, self.prior4pC, self.priorHBL, self.priorHBLD, self.priorSpeed, self.priorAcce, self.priorCurve, self.priorJoystickSpeed, self.priorjoystickEnable, self.priorEncoderEnable, self.priorJX, self.priorJY, self.priorXD, self.priorYD, self.priorMicroStep, self.priorXfields, self.priorYfields, self.priorTimeInter, self.priorRepeat, self.recordTime, self.stopPrior = paramas().paramaSetting()

    def signalslots(self):
        self.ui.start.clicked.connect(self.camOpen)
        self.ui.stop.clicked.connect(self.camClose)
        self.ui.capture.clicked.connect(self.updateImage)
        self.ui.save.clicked.connect(self.saveImage)
        self.ui.back.clicked.connect(self.goback)
        self.ui.forward.clicked.connect(self.goforward)
        self.ui.left.clicked.connect(self.goleft)
        self.ui.right.clicked.connect(self.goright)
        self.ui.up.clicked.connect(self.goup)
        self.ui.down.clicked.connect(self.godown)
        self.ui.home.clicked.connect(self.goHome)
        self.ui.refresh.clicked.connect(self.refreshT)
        self.ui.record.clicked.connect(camRecord)
        self.ui.priorGoto.clicked.connect(self.priorScan)
        self.ui.actionSutter_MP285.triggered.connect(self.createSubWin1)
        self.ui.save.setEnabled(False)
        self.ui.Priorhome.clicked.connect(self.priorHome)
        self.ui.priorStop.clicked.connect(self.priorStop)
        self.ui.actionPrior_controller.triggered.connect(self.createSubwin2)
        self.ui.actionBasler_camera.triggered.connect(self.createSubwin3)
        self.ui.actionDevices_connections.triggered.connect(self.createSubwin4)
        self.ui.priorPx.clicked.connect(self.priorPX)
        self.ui.priorPy.clicked.connect(self.priorPY)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()

    # overload functions
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            if self.FlagP == 0 & self.FlagS == 0:
                self.FlagP = 1
                try:
                    move = self.prior.moveForward()
                    self.ui.messagbox.append(move)
                except:
                    self.ui.messagbox.append("Error in Prior.Please check the connection.")
                self.FlagP = 0
            else:
                self.ui.messagbox.append("Other function processing")
        elif e.key() == Qt.Key_Down:
            if self.FlagP == 0 & self.FlagS == 0:
                self.FlagP = 1
                try:
                    move = self.prior.moveBack()
                    self.ui.messagbox.append(move)
                except:
                    self.ui.messagbox.append("Error in Prior.Please check the connection.")
                self.FlagP = 0
            else:
                self.ui.messagbox.append("Other function processing")
        elif e.key() == Qt.Key_Left:
            if self.FlagP == 0 & self.FlagS == 0:
                self.FlagP = 1
                try:
                    move = self.prior.moveLeft()
                    self.ui.messagbox.append(move)
                except:
                    self.ui.messagbox.append("Error in Prior.Please check the connection.")
                self.FlagP = 0
            else:
                self.ui.messagbox.append("Other function processing")
        elif e.key() == Qt.Key_Right:
            if self.FlagP == 0 & self.FlagS == 0:
                self.FlagP = 1
                try:
                    move = self.prior.moveRight()
                    self.ui.messagbox.append(move)
                except:
                    self.ui.messagbox.append("Error in Prior.Please check the connection.")
                self.FlagP = 0
            else:
                self.ui.messagbox.append("Other function processing")

    def mouseMoveEvent(self, event):
        if self.ui.Frame.underMouse():
            self.pos = [(event.localPos().x() - 20), (event.localPos().y() - 106)]
            self.ui.coordinate.setText(str(self.pos[0]) + "," + str(self.pos[1]))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.cam.StopGrabbing()
            self.cam.Close()
            MP285.exitFlag = Prior.exitFlag = 1
            print('over')
        else:
            event.ignore()

    def refreshT(self):
        if self.FlagS == 0 and self.FlagP == 0:
            self.ui.messagbox.append('Reconnecting')
            self.FlagP = 1
            self.FlagS = 1
            pool = QThreadPool.globalInstance()
            runnable = Runnable(self.refresh)
            runnable.setAutoDelete(True)
            pool.start(runnable)
        else:
            self.ui.messagbox.append('Other function is processing')

    def refresh(self):
        if self.CAME == 1:
            self.connectCam()
        else:
            pass
        if self.SCE == 1:
            self.connectSutter()
            if self.SCE == 0:
                pool = QThreadPool.globalInstance()
                runnable = Runnable(self.setSutterData)
                runnable.setAutoDelete(True)
                pool.start(runnable)
        else:
            pass
        if self.PCE == 1:
            self.connectController()
            if self.PCE == 0:
                pool = QThreadPool.globalInstance()
                runnable = Runnable(self.setPriorData)
                runnable.setAutoDelete(True)
                pool.start(runnable)
        else:
            pass
        self.ui.messagbox.append('Reconnect completed')
        self.FlagP = 0
        self.FlagS = 0

    # initialize connection
    def connectSutter(self):
        self.comS = 8
        try:
            self.sutter = MP285(self.comS)
            self.ui.messagbox.append("MP is connected")
            self.SCE = 0
        except Exception as ex:
            self.ui.messagbox.append("Error," + str(ex))
            self.SCE = 1

    def connectController(self):
        self.comP = 7
        try:
            self.prior = Prior(self.comP)
            self.ui.messagbox.append("Prior is connected")
            self.PCE = 0
        except Exception as ex:
            self.ui.messagbox.append("Error," + str(ex))
            self.PCE = 1

    def connectCam(self):
        try:
            self.tlf = pylon.TlFactory.GetInstance()
            # Getting the instance of the transport layer
            self.cam = pylon.InstantCamera()
            # create an InstantCamera object
            self.cam.Attach(self.tlf.CreateFirstDevice())
            # The connection between the wrapper object InstantCamera and the actual device happens when we Attach it
            self.cam.Open()
            nodeFile = "NodeMap.pfs"
            pylon.FeaturePersistence.Load(nodeFile, self.cam.GetNodeMap(), True)
            self.CAME = 0
            self.ui.messagbox.append("Initialize camera")
            self.ui.capture.setEnabled(True)
            self.ui.start.setEnabled(True)
            self.ui.stop.setEnabled(True)
            self.ui.record.setEnabled(True)
        except:
            self.ui.messagbox.append('Error in camera')
            self.CAME = 1
            self.ui.capture.setEnabled(False)
            self.ui.start.setEnabled(False)
            self.ui.stop.setEnabled(False)
            self.ui.record.setEnabled(False)

    def createSubwin3(self):
        self.winBasler = BaslerWindow()
        self.winBasler.sub.spinBox_2.setValue(self.recordTime)
        self.winBasler.show()
        self.winBasler.process2.currentReTime.connect(self.resetRecordTime)

    def resetRecordTime(self, reT):
        if reT != self.recordTime:
            self.recordTime = reT
        else:
            pass

    def createSubwin4(self):
        self.winDevices = DevicesWindow()
        self.winDevices.show()

    def createSubwin2(self):
        self.winPrior = PriorWindow()
        self.pE = 0
        self.setPrior()
        self.winPrior.show()
        self.winPrior.process1.currentPrior.connect(self.resetP)

    def resetP(self, p=()):
        self.p = p
        if self.FlagP == 1:
            self.ui.messagbox.append('Prior is processing')
            pass
        else:
            pool = QThreadPool.globalInstance()
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(self.resetPrior)
            runnable.setAutoDelete(True)
            # 3. Call start()
            pool.start(runnable)

    def resetPrior(self):
        d, s, j, o, pa = self.p
        self.FlagP = 1
        if d[0] != self.priorStepSizeX or d[1] != self.priorStepSizeY:
            try:
                self.pE = self.prior.setStep(d[0], d[1])
                if self.pE == 0:
                    self.priorStepSizeX = d[0]
                    self.priorStepSizeY = d[1]
            except:
                self.pE = 1
        if d[2] != self.prior4pC:
            try:
                self.pE = self.prior.correctionEnable(d[2])
                if self.pE == 0:
                    self.prior4pC = d[2]
            except:
                self.pE = 1
        if d[3] != self.priorHBL:
            try:
                self.pE = self.prior.HostBackLashEnable(d[3], d[4])
                if self.pE == 0:
                    self.priorHBL = d[3]
                    self.priorHBLD = d[4]
            except:
                self.pE = 1
        if s[0] != self.priorSpeed:
            try:
                self.pE = self.prior.setSpeed(s[0])
                if self.pE == 0:
                    self.priorSpeed = s[0]
            except:
                self.pE = 1
        if s[1] != self.priorAcce:
            try:
                self.pE = self.prior.setAcceleration(s[1])
                if self.pE == 0:
                    self.priorAcce = s[1]
            except:
                self.pE = 1
        if s[2] != self.priorCurve:
            try:
                self.pE = self.prior.setCurve(s[2])
                if self.pE == 0:
                    self.priorCurve = s[2]
            except:
                self.pE = 1
        if j[0] != self.priorJoystickSpeed:
            try:
                self.pE = self.prior.setJoystickSpeed(j[0])
                if self.pE == 0:
                    self.priorJoystickSpeed = j[0]
            except:
                self.pE = 1
        if j[1] != self.priorJX:
            try:
                self.pE = self.prior.joystickXreverse(j[1])
                if self.pE == 0:
                    self.priotJX = j[1]
            except:
                self.pE = 1
        if j[2] != self.priorJY:
            try:
                self.pE = self.prior.joystickYreverse(j[2])
                if self.pE == 0:
                    self.priorJY = j[2]
            except:
                self.pE = 1
        if j[3] != self.priorXD:
            try:
                self.pE = self.prior.hostXreverse(j[3])
                if self.pE == 0:
                    self.priorXD = j[3]
            except:
                self.pE = 1
        if j[4] != self.priorYD:
            try:
                self.pE = self.prior.hostYreverse(j[4])
                if self.pE == 0:
                    self.priorYD = j[4]
            except:
                self.pE = 1
        if j[5] != self.priorjoystickEnable:
            try:
                self.pE = self.prior.joystickSetEnable(j[5])
                if self.pE == 0:
                    self.priorjoystickEnable = j[5]
            except:
                self.pE = 1
        if o[0] != self.priorMicroStep:
            try:
                self.pE = self.prior.setMicroStep(o[0])
                if self.pE == 0:
                    self.priorMicroStep = o[0]
            except:
                self.pE = 1
        if o[1] != self.priorEncoderEnable:
            try:
                self.pE = self.prior.encoderEnable(o[1])
                if self.pE == 0:
                    self.priorEncoderEnable = o[1]
            except:
                self.pE = 1
        if pa[0] != self.priorXfields or pa[1] != self.priorYfields:
            try:
                self.pE = self.prior.setPatternFields(pa[0], pa[1])
                if self.pE == 0:
                    self.priorXfields = pa[0]
                    self.priorYfields = pa[1]
            except:
                self.pE = 1
        if pa[2] != self.priorTimeInter:
            self.priorTimeInter = pa[2]
        if pa[3] != self.priorRepeat:
            self.priorRepeat = pa[3]
        if self.pE != 0:
            self.ui.messagbox.append('Some parameters of Prior fail to reset')
            self.pE = 0
        else:
            self.ui.messagbox.append('Prior reset finish')
        self.FlagP = 0

    def setPriorData(self):
        try:
            self.ui.messagbox.append('Setting prior')
            self.setupPriorDefault(self.priorStepSizeX, self.priorStepSizeY, self.prior4pC, self.priorHBL,
                                   self.priorHBLD)
            self.setupPriorStage(self.priorSpeed, self.priorAcce, self.priorCurve)
            self.setupPriorJoystick(self.priorJoystickSpeed, self.priorJX, self.priorJY, self.priorXD, self.priorYD,
                                    self.priorjoystickEnable)
            self.setupPriorOthers(self.priorMicroStep, self.priorEncoderEnable)
            self.setupPattern()
            self.ui.messagbox.append('Prior is set')
        except:
            self.ui.messagbox.append('Fail to setup Prior')
        self.FlagP = 0

    def setupPattern(self):
        self.prior.Pattern(self.priorXfields, self.priorYfields)

    def setupPriorDefault(self, u, v, correctF, HBL, HBLD):
        self.prior.setStep(u, v)
        self.prior.correctionEnable(correctF)
        self.prior.HostBackLashEnable(HBL, HBLD)

    def setupPriorStage(self, s, a, c):
        self.prior.setSpeed(s)
        self.prior.setAcceleration(a)
        self.prior.setCurve(c)

    def setupPriorJoystick(self, s, jx, jy, hx, hy, je):
        self.prior.setJoystickSpeed(s)
        self.prior.joystickXreverse(jx)
        self.prior.joystickYreverse(jy)
        self.prior.hostXreverse(hx)
        self.prior.hostYreverse(hy)
        self.prior.joystickSetEnable(je)

    def setupPriorOthers(self, s, f):
        self.prior.setMicroStep(s)
        self.prior.encoderEnable(f)

    def setPrior(self):
        self.winPrior.sub.stepSizeX.setValue(self.priorStepSizeX)
        self.winPrior.sub.stepSizeY.setValue(self.priorStepSizeY)
        if self.prior4pC == 1:
            self.winPrior.sub.correction4P.setChecked(True)
        else:
            self.winPrior.sub.correction4P.setChecked(False)
        if self.priorHBL == 1:
            self.winPrior.sub.HBLenable.setChecked(True)
        else:
            self.winPrior.sub.HBLenable.setChecked(False)
        self.winPrior.sub.HBLD.setValue(self.priorHBLD)
        self.winPrior.sub.speed.setValue(self.priorSpeed)
        self.winPrior.sub.acceleteation.setValue(self.priorAcce)
        self.winPrior.sub.curve.setValue(self.priorCurve)
        self.winPrior.sub.joySpeed.setValue(self.priorJoystickSpeed)
        if self.priorjoystickEnable == 1:
            self.winPrior.sub.joystickEnable.setChecked(True)
        else:
            self.winPrior.sub.joystickEnable.setChecked(False)
        if self.priorEncoderEnable == 1:
            self.winPrior.sub.encoderEnable.setChecked(True)
        else:
            self.winPrior.sub.encoderEnable.setChecked(False)
        if self.priorJX == 1:
            self.winPrior.sub.joyXrever.setChecked(False)
        else:
            self.winPrior.sub.joyXrever.setChecked(True)
        if self.priorJY == 1:
            self.winPrior.sub.joyYrever.setChecked(False)
        else:
            self.winPrior.sub.joyYrever.setChecked(True)
        if self.priorXD == 1:
            self.winPrior.sub.HostXrever.setChecked(False)
        else:
            self.winPrior.sub.HostYrever.setChecked(True)
        if self.priorYD == 1:
            self.winPrior.sub.HostYrever.setChecked(False)
        else:
            self.winPrior.sub.HostYrever.setChecked(True)
        self.winPrior.sub.microStep.setValue(self.priorMicroStep)
        self.winPrior.sub.xFields.setValue(self.priorXfields)
        self.winPrior.sub.yFields.setValue(self.priorYfields)
        self.winPrior.sub.timeInter.setValue(self.priorTimeInter)
        self.winPrior.sub.repeat.setValue(self.priorRepeat)

    def priorPX(self):
        re = self.prior.setPXzero()
        self.ui.messagbox.append(re)

    def priorPY(self):
        re2 = self.prior.setPYzero()
        self.ui.messagbox.append(re2)

    def priorScan(self):
        if self.ui.priorAutoMove.isChecked():
            pool = QThreadPool.globalInstance()
            runnable = Runnable(self.priorAutoMove)
            runnable.setAutoDelete(True)
            pool.start(runnable)
        else:
            pool = QThreadPool.globalInstance()
            runnable = Runnable(self.priorManulScan)
            runnable.setAutoDelete(True)
            pool.start(runnable)

    def priorAutoMove(self):
        self.ui.messagbox.append('Prior begin to auto scan')
        self.FlagP = 1
        self.ui.priorGoto.setEnabled(False)
        for rp in range(self.priorRepeat + 1):
            self.prior.Pattern(self.priorXfields, self.priorYfields)
            s = (self.priorXfields + 1) * (self.priorYfields + 1) - 1
            for i in range(s):
                self.prior.manulMove(self.priorTimeInter)
                self.ui.messagbox.append('Prior auto scan, step number %d' % i)
                if self.ui.priorAutoImage.isChecked():
                    self.updateImage()
                    self.saveImage()
                if self.stopPrior == 1:
                    break
            if rp != self.priorRepeat:
                self.ui.messagbox.append('Repeat auto scan')
            if self.stopPrior == 1:
                break
        self.stopPrior = 0
        self.ui.messagbox.append('Prior auto scan finished')
        self.FlagP = 0
        self.ui.priorGoto.setEnabled(True)

    def priorManulScan(self):
        respond = self.prior.manulMove(self.priorTimeInter)
        self.ui.messagbox.append(respond)

    def priorHome(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagP = 1
            try:
                act = self.prior.goHome()
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Prior.Please check the connection.')
            self.FlagP = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def priorStop(self):
        if self.ui.priorAutoMove.isChecked():
            self.stopPrior = 1
            self.ui.priorGoto.setEnabled(True)
        else:
            try:
                act = self.prior.moveStop()
                self.ui.messagbox.append(act)
                self.FlagP = 0
            except:
                self.ui.messagbox.append('Error in Prior.Please check the connection.')
                if self.FlagP != 0:
                    try:
                        act1 = self.prior.suddenStop()
                        self.ui.messagbox.append(
                            act1)
                    except:
                        self.ui.messagbox.append('Prior fail to sudden stop')

    def createSubWin1(self):
        self.winSutter = SutterWindow()
        self.SE = 0
        self.setSutter(self.vel, self.res, self.stepL)
        self.winSutter.show()
        self.winSutter.Process.currentSutter.connect(self.resetS)

    def setSutterData(self):
        self.vel = 200
        self.res = 0
        self.FlagS = 1
        self.stepL = 1
        self.ui.messagbox.append('Sutter is setting')
        try:
            b = self.sutter.setVelocity(self.vel, self.res)
            if b == 0:
                self.ui.messagbox.append('Sutter setting finish')
        except:
            self.ui.messagbox.append('Fail to setup Sutter')
        self.FlagS = 0

    def setSutter(self, vel, Res, step):
        self.winSutter.subui.velocity.setValue(vel)
        if Res == 1:
            self.winSutter.subui.ResH.setChecked(True)
        else:
            self.winSutter.subui.ResH.setChecked(False)
        self.winSutter.subui.stepSize.setValue(step)

    def resetS(self, s):
        self.s = s
        if self.FlagS == 1:
            self.ui.messagbox.append('Other function is processing')
        else:
            pool = QThreadPool.globalInstance()
            runnable = Runnable(self.resetSutter)
            runnable.setAutoDelete(True)
            pool.start(runnable)
            runnable.autoDelete()

    def resetSutter(self):
        self.FlagS = 1
        if self.s[0] != self.vel or self.s[1] != self.res:
            if self.s[0] <= 3000 and self.s[1] == 0:
                try:
                    self.SE = self.sutter.setVelocity(self.s[0], self.s[1])
                    if self.SE == 0:
                        self.vel = self.s[0]
                        self.res = self.s[1]
                except:
                    self.SE = 1

            if self.s[0] > 3000 and self.s[1] == 0:
                self.ui.messagbox.append('Sutter:Please input a velocity less than 3000')
                self.SE = 1
            if self.s[0] <= 1310 and self.s[1] == 1:
                try:
                    self.SE = self.sutter.setVelocity(self.s[0], self.s[1])
                    if self.SE == 0:
                        self.vel = self.s[0]
                        self.res = self.s[1]
                except:
                    self.SE = 1

            if self.s[0] > 1310 and self.s[1] == 1:
                self.ui.messagbox.append('Sutter:Please input a velocity less than 1310')
                self.SE = 1

        if self.s[2] != self.stepL:
            if self.res == 1:
                if (self.s[2] * 25) % 1 == 0:
                    self.stepL = self.s[2]
                else:
                    self.ui.messagbox.append('Sutter:Please input multiples of 0.04')
                    self.SE = 1
            elif self.res == 0:
                if (self.s[2] * 5) % 1 == 0:
                    self.stepL = self.s[2]
                else:
                    self.SE = 1
                    self.ui.messagbox.append('Sutter:Please input multiples of 0.2')
        if self.SE == 1:
            self.ui.messagbox.append('Fail to reset Sutter')
            self.SE = 0
        else:
            self.ui.messagbox.append('Sutter reset finish')
        self.FlagS = 0

    # SutterMP285 events
    def goforward(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goForward(self.stepL)
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def goback(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goBack(self.stepL)
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def goleft(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goLeft(self.stepL)
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def goright(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goRight(self.stepL)
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def goup(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goUp(self.stepL)
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def godown(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goDown(self.stepL)
                self.ui.messagbox.append(act)
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    def goHome(self):
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagS = 1
            try:
                act = self.sutter.goHome()
                self.ui.messagbox.append(act[0])
            except:
                self.ui.messagbox.append('Error in Sutter.Please check the connection.')
            self.FlagS = 0
        else:
            self.ui.messagbox.append("Other function processing")

    # camera events
    def camOpen(self):
        self.ui.start.setEnabled(False)
        self.ui.stop.setEnabled(True)
        self.ui.save.setEnabled(False)
        self.ui.capture.setEnabled(False)
        self.ui.menuSettings.setEnabled(False)
        if self.ui.priorAutoImage.isChecked():
            self.ui.messagbox.append('Images cannot be saved when recording')
            self.ui.priorAutoImage.setChecked(False)
        thcam = threading.Thread(target=self.camDisplay)
        thcam.start()

    def camClose(self):
        self.stopEvent.set()

    def updateImage(self):
        img = []
        self.FlagImg = 1
        self.cam.StartGrabbing(1)
        grab = self.cam.RetrieveResult(2000, pylon.TimeoutHandling_Return)
        if grab.GrabSucceeded():
            # check the grab work
            self.ui.save.setEnabled(True)
            self.setMouseTracking(True)
            image = converter.Convert(grab)
            img = image.GetArray()
            img1 = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            self.ui.Frame.setPixmap(QPixmap.fromImage(img1))
        grab.Release()
        self.cam.StopGrabbing()
        return img

    def camDisplay(self):
        # self.cam.StartGrabbingMax(12000,pylon.GrabStrategy_LatestImageOnly)
        self.cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        while self.cam.IsGrabbing():
            grabResult = self.cam.RetrieveResult(3000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)
                img = image.GetArray()
                if self.is_running:
                    self.frame_queue.put(img)
                img2 = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                self.ui.Frame.setPixmap(QPixmap.fromImage(img2))
            grabResult.Release()
            if self.stopEvent.is_set():
                grabResult.Release()
                self.cam.StopGrabbing()
                self.is_running = False
                self.stopEvent.clear()
                break
        grabResult.Release()
        self.ui.start.setEnabled(True)
        self.FlagImg = 1
        self.ui.save.setEnabled(True)
        self.ui.menuSettings.setEnabled(True)
        self.ui.capture.setEnabled(True)

    def saveImage(self):
        if self.FlagImg == 1:
            frame = self.updateImage()
            self.img = frame.copy()
            self.FlagImg = 0
            img1 = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        else:
            img1 = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        if self.ui.priorAutoImage.isChecked():
            fd = expFileMaxNum('sperm_sample', './test/', 'autoImages') + '.png'
        else:
            fd, type = QFileDialog.getSaveFileName(None, "Save image", "", "*.png;;*.jpg;;All Files(*)")
        img1.save(fd)


def expFileMaxNum(FileName, FolderPath, Layer):
    FolderPath = FolderPath + '/%s' % (Layer)
    Path(FolderPath).mkdir(parents=True, exist_ok=True)
    FileList = glob.glob(FolderPath + '/*')
    if len(FileList) == 0:
        FileCount = 1
    else:
        MaxNum = 0
        for idx in range(len(FileList)):
            temp = re.findall('\d+', FileList[idx])
            temp_list = map(int, temp)
            temp1 = max(temp_list) + 1
            if MaxNum < temp1:
                MaxNum = temp1
        FileCount = MaxNum

    DestPath = '%s/%s_%d' % (FolderPath, FileName, FileCount)
    return DestPath


def camRecord():
    fdefault = expFileMaxNum('sperm_sample', './test/', 'test1')
    if MainWindow.cam.IsGrabbing():
        pass
    else:
        MainWindow.camOpen()

    MainWindow.ui.record.setEnabled(False)
    if not MainWindow.ui.AutoRecord.isChecked():
        fdm = QFileDialog.getSaveFileName(None, "Save Video", "", "*.avi;;All Files(*)")
        if fdm[0] == (''):
            MainWindow.is_running = False
            MainWindow.ui.record.setEnabled(True)
            pass
        else:
            MainWindow.is_running = True
            fd = fdm[0]
            thcam = threading.Thread(target=RecordVideo, args=(frame_queue, fd,))
            thcam.daemon = True
            thcam.start()
    else:
        MainWindow.is_running = True
        fd2 = fdefault
        fd = fd2 + '.avi'
        tht = threading.Thread(target=AutoStop)
        tht.daemon = True
        tht.start()
        thcam = threading.Thread(target=RecordVideo, args=(frame_queue, fd,))
        thcam.daemon = True
        thcam.start()


def AutoStop():
    if MainWindow.ui.priorAutoMove.isChecked():
        try:
            MainWindow.ui.priorGoto.setEnabled(False)
            MainWindow.priorAutoMove()
        except:
            MainWindow.ui.messagbox.append('Prior fail to auto move when recording')
    else:
        time.sleep(MainWindow.recordTime)
    if MainWindow.is_running:
        MainWindow.camClose()
    else:
        pass
    MainWindow.ui.priorGoto.setEnabled(True)


def RecordVideo(frame, fd):
    fps = 24  # Hz
    time = 30  # seconds
    maxImage = 2400
    if maxImage <= fps * time:
        print('number error ,pass')
        pass
    else:
        writer = get_writer(
            (fd),  # mkv players often support H.264
            fps=fps,  # FPS is in units Hz; should be real-time.
            codec='libx264',  # When used properly, this is basically "PNG for video" (i.e. lossless)
            quality=None,  # disables variable compression
            ffmpeg_params=[  # compatibility with older library versions
                '-preset',  # set to fast, faster, veryfast, superfast, ultrafast
                'fast',  # for higher speed but worse compression
                '-crf',  # quality; set to 0 for lossless, but keep in mind
                '24'  # that the camera probably adds static anyway
            ]
        )
        while True:
            image = frame.get()
            writer.append_data(image)
            if MainWindow.stopEvent.is_set():
                MainWindow.ui.record.setEnabled(True)
                break
        frame_queue.task_done()
        MainWindow.ui.messagbox.append("Record Done.\nVideo can be found later in the floder")
        MainWindow.ui.AutoRecord.setEnabled(True)


if __name__ == "__main__":
    converter = pylon.ImageFormatConverter()
    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    app = QApplication(sys.argv)
    frame_queue = queue.Queue()
    MainWindow = Window(frame_queue)
    MainWindow.show()
    th1 = threading.Thread(target=MainWindow.setPriorData)
    th1.start()
    th1.join()
    th2 = threading.Thread(target=MainWindow.setSutterData)
    th2.start()
    th2.join()
    sys.exit(app.exec_())
