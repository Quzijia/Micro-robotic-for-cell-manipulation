import queue
import sys
import threading
import time
import re
import glob
from multiprocessing import Queue, Process, Pipe
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QRunnable, QThread, pyqtSlot, QThreadPool
from PyQt5.QtGui import QImage, QPixmap
from imageio import get_writer
from UIwindow import Ui_MainWindow
from Prior import Prior
from Sutter import MP285
import pypylon.pylon as pylon
from SubwinS import Ui_Dialog
from SubwinP import Ui_Dialog2


class PriorWindow(QDialog):
    def __init__(self):
        super(PriorWindow, self).__init__()
        self.sub = Ui_Dialog2()
        self.sub.setupUi(self)
        self.process1 = Worksignal()

    def accept(self):
        xStep = self.sub.stepSizeX.value()
        yStep = self.sub.stepSizeY.value()
        if self.sub.correction4P.isChecked():
            c = 1
        else:
            c = 0
        if self.sub.HBLenable.isChecked():
            h = 1
        else:
            h = 0
        HBLD = self.sub.HBLD.value()
        default = [xStep, yStep, c, h, HBLD]
        # self.process1.currentPriorDefault.emit(default)
        s = self.sub.speed.value()
        a = self.sub.acceleteation.value()
        c = self.sub.curve.value()
        stage = [s, a, c]
        # self.process1.currentPriorDefault.emit(stage)
        js = self.sub.joySpeed.value()
        if self.sub.joyXrever.isChecked():
            jx = -1
        else:
            jx = 1
        if self.sub.joyYrever.isChecked():
            jy = -1
        else:
            jy = 1
        if self.sub.HostXrever.isChecked():
            hx = -1
        else:
            hx = 1
        if self.sub.HostYrever.isChecked():
            hy = -1
        else:
            hy = 1
        if self.sub.joystickEnable.isChecked():
            je = 1
        else:
            je = 0
        joy = [js, jx, jy, hx, hy, je]
        # self.process1.currentPriorJoystick.emit(joy)
        ms = self.sub.microStep.value()
        if self.sub.encoderEnable.isChecked():
            ee = 1
        else:
            ee = 0
        other = [ms, ee]
        # self.process1.currentPriorOther.emit(other)
        self.process1.currentPrior.emit((default, stage, joy, other))
        self.close()


class SutterWindow(QDialog):
    def __init__(self):
        super(SutterWindow, self).__init__()
        self.subui = Ui_Dialog()
        self.subui.setupUi(self)
        self.Process = Worksignal()

    def accept(self):
        vel = self.subui.velocity.value()
        if self.subui.ResH.isChecked():
            res = 1
        else:
            res = 0
        step = self.subui.stepSize.value()
        l = [vel, res, step]
        self.Process.currentSutter.emit(l)
        self.close()


class Worksignal(QObject):
    currentSutter = pyqtSignal(list)
    currentPrior = pyqtSignal(tuple)


# 1. Subclass QRunnable
class Runnable(QRunnable):
    def __init__(self, n, fn):
        super().__init__()
        self.n = n
        self.fn = fn

    def run(self):
        self.fn()


class Window(QMainWindow):
    def __init__(self, frame_queue):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.signalslots()
        # self.setMouseTracking(True)
        self.connectCam()
        self.connectController()
        self.connectSutter()
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.FlagP = 0
        # prior
        self.FlagS = 0
        # sutter
        self.FlagImg = 0

        self.frame_queue = frame_queue  # 帧队列
        self.is_running = False  # 状态标签

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
        self.ui.actionSutter_MP285.triggered.connect(self.createSubWin1)
        self.ui.save.setEnabled(False)
        self.ui.Priorhome.clicked.connect(self.priorHome)
        self.ui.priorStop.clicked.connect(self.priorStop)
        self.ui.actionPrior_controller.triggered.connect(self.createSubwin2)
        # 创建一个关闭事件并设为未触发

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
            self.pos = event.localPos()
            self.ui.coordinate.setText(str((event.localPos().x()) - 20) + "," + str((event.localPos().y()) - 80))
            # self.update()
        else:
            pass

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

            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(0, self.refresh)
            # 3. Call start()
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
                # 2. Instantiate the subclass of QRunnable
                runnable = Runnable(1, self.setSutterData)
                # 3. Call start()
                pool.start(runnable)
        else:
            pass
        if self.PCE == 1:
            self.connectController()
            if self.PCE == 0:
                pool = QThreadPool.globalInstance()
                # 2. Instantiate the subclass of QRunnable
                runnable = Runnable(2, self.setPriorData)
                # 3. Call start()
                pool.start(runnable)
        else:
            pass
        self.ui.messagbox.append('Reconnect completed')
        self.FlagP = 0
        self.FlagS = 0

    # initialize connection
    def connectSutter(self):
        try:
            self.sutter = MP285()
            self.ui.messagbox.append("MP is connected")
            self.SCE = 0
        except Exception as ex:
            self.ui.messagbox.append("Error," + str(ex))
            self.SCE = 1

    def connectController(self):
        try:
            self.prior = Prior()
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

    def createSubwin2(self):
        self.winPrior = PriorWindow()
        self.pE = 0
        self.setPrior()
        self.winPrior.show()
        # self.winPrior.process1.currentPriorDefault.connect(self.resetPDefault)
        # self.winPrior.process1.currentPriorStage.connect(self.resetPStage)
        # self.winPrior.process1.currentPriorJoystick.connect(self.resetPJoy)
        # self.winPrior.process1.currentPriorOther.connect(self.resetPOther)
        self.winPrior.process1.currentPrior.connect(self.resetP)

    def resetP(self, p = ()):
        self.p = p
        if self.FlagP == 1:
            self.ui.messagbox.append('Prior is processing')
            pass
        else:
            pool = QThreadPool.globalInstance()
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(2, self.resetPrior)
            # 3. Call start()
            pool.start(runnable)

    def resetPrior(self):
        d = self.p[0]
        s = self.p[1]
        j = self.p[2]
        o = self.p[3]
        self.FlagP = 1
        if d[0] != self.priorStepSizeX:
            if d[1] != self.priorStepSizeY:
                try:
                    self.pE = self.prior.setStep(d[0], d[1])
                    if self.pE == 0:
                        self.priorStepSizeX = d[0]
                        self.priorStepSizeY = d[1]
                except:
                    self.pE = 1

        elif d[1] == self.priorStepSizeY:
            try:
                self.pE = self.prior.setStep(d[0], self.priorStepSizeY)
                if self.pE == 0:
                    self.priorStepSizeX = d[0]
            except:
                self.pE = 1
        else:
            if d[1] != self.priorStepSizeY:
                # self.priorStepSizeY = d[1]
                try:
                    self.pE = self.prior.setStep(self.priorStepSizeX, d[1])
                    if self.pE == 0:
                        self.priorStepSizeY = d[1]
                except:
                    self.pE = 1
            else:
                pass
        if d[2] != self.prior4pC:
            # self.prior4pC = d[2]
            try:
                self.pE = self.prior.correctionEnable(d[2])
                if self.pE == 0:
                    self.prior4pC = d[2]
            except:
                self.pE = 1
                pass
        else:
            pass
        if d[3] != self.priorHBL:
            # self.priorHBL = d[3]
            # self.priorHBLD = d[4]
            try:
                self.pE = self.prior.HostBackLashEnable(d[3], d[4])
                if self.pE == 0:
                    self.priorHBL = d[3]
                    self.priorHBLD = d[4]
            except:
                self.pE = 1
                pass
        else:
            pass
        if s[0] != self.priorSpeed:
            # self.priorSpeed = s[0]
            try:
                self.pE = self.prior.setSpeed(s[0])
                if self.pE == 0:
                    self.priorSpeed = s[0]
            except:
                self.pE = 1
                pass
        else:
            pass
        if s[1] != self.priorAcce:
            # self.priorAcce = s[1]
            try:
                self.pE = self.prior.setAcceleration(s[1])
                if self.pE == 0:
                    self.priorAcce = s[1]
            except:
                self.pE = 1
                pass
        if s[2] != self.priorCurve:
            # self.priorCurve = s[2]
            try:
                self.pE = self.prior.setCurve(s[2])
                if self.pE == 0:
                    self.priorCurve = s[2]
            except:
                self.pE = 1
                pass
        else:
            pass
        if j[0] != self.priorJoystickSpeed:
            # self.priorJoystickSpeed = j[0]
            try:
                self.pE = self.prior.setJoystickSpeed(j[0])
                if self.pE == 0:
                    self.priorJoystickSpeed = j[0]
            except:
                self.pE = 1
        else:
            pass
        if j[1] != self.priorJX:
            # self.priotJX = j[1]
            try:
                self.pE = self.prior.joystickXreverse(j[1])
                if self.pE == 0:
                    self.priotJX = j[1]
            except:
                self.pE = 1
                pass
        else:
            pass
        if j[2] != self.priorJY:
            # self.priorJY = j[2]
            try:
                self.pE = self.prior.joystickYreverse(j[2])
                if self.pE == 0:
                    self.priorJY = j[2]
            except:
                self.pE = 1
                pass
        else:
            pass
        if j[3] != self.priorXD:
            # self.priorXD = j[3]
            try:
                self.pE = self.prior.hostXreverse(j[3])
                if self.pE == 0:
                    self.priorXD = j[3]
            except:
                self.pE = 1
                pass
        else:
            pass
        if j[4] != self.priorYD:
            # self.priorYD = j[4]
            try:
                self.pE = self.prior.hostYreverse(j[4])
                if self.pE == 0:
                    self.priorYD = j[4]
            except:
                self.pE = 1
                pass
        else:
            pass
        if j[5] != self.priorjoystickEnable:
            # self.priorjoystickEnable = j[5]
            try:
                self.pE = self.prior.joystickSetEnable(j[5])
                if self.pE == 0:
                    self.priorjoystickEnable = j[5]
            except:
                self.pE = 1
                pass
        else:
            pass

        if o[0] != self.priorMicroStep:
            # self.priorMicroStep = o[0]
            try:
                self.pE = self.prior.setMicroStep(o[0])
                if self.pE == 0:
                    self.priorMicroStep = o[0]
            except:
                self.pE = 1
                pass
        else:
            pass
        if o[1] != self.priorEncoderEnable:
            # self.priorEncoderEnable = o[1]
            try:
                self.pE = self.prior.encoderEnable(o[1])
                if self.pE == 0:
                    self.priorEncoderEnable = o[1]
            except:
                self.pE = 1
                pass
        if self.pE != 0:
            self.ui.messagbox.append('Some parameters of Prior fail to reset')
            self.pE = 0
        else:
            self.ui.messagbox.append('Prior reset finish')
        self.FlagP = 0

    def setPriorData(self):
        self.FlagP = 1
        self.priorStepSizeX = 1000
        self.priorStepSizeY = 1000
        self.prior4pC = 1
        self.priorHBL = 1
        self.priorHBLD = 100
        self.priorSpeed = 6000
        self.priorAcce = 28550
        self.priorCurve = 100
        self.priorJoystickSpeed = 100
        self.priorjoystickEnable = 1
        self.priorEncoderEnable = 1
        self.priorJX = 1
        self.priorJY = 1
        self.priorXD = 1
        self.priorYD = 1
        self.priorMicroStep = 100
        try:
            self.ui.messagbox.append('Setting prior')
            self.setupPriorDefault(self.priorStepSizeX, self.priorStepSizeY, self.prior4pC, self.priorHBL,
                                   self.priorHBLD)
            self.setupPriorStage(self.priorSpeed, self.priorAcce, self.priorCurve)
            self.setupPriorJoystick(self.priorJoystickSpeed, self.priorJX, self.priorJY, self.priorXD, self.priorYD,
                                    self.priorjoystickEnable)
            self.setupPriorOthers(self.priorMicroStep, self.priorEncoderEnable)
            self.ui.messagbox.append('Prior is set')
        except:
            self.ui.messagbox.append('Fail to setup Prior')
        self.FlagP = 0

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
        if self.FlagP == 0 & self.FlagS == 0:
            self.FlagP = 1
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
                self.FlagP = 0
        else:
            self.ui.messagbox.append("Other function processing")

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
            self.sutter.goHome()
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

    def resetS(self, s = []):
        self.s = s
        if self.FlagS == 1:
            self.ui.messagbox.append('Other function is processing')
        else:
            pool = QThreadPool.globalInstance()
            # 2. Instantiate the subclass of QRunnable
            runnable = Runnable(1, self.resetSutter)
            # 3. Call start()
            pool.start(runnable)

    def resetSutter(self):
        self.FlagS = 1
        if self.s[0] != self.vel:
            if self.s[1] != self.res and self.s[1] == 0:
                if self.s[0] <= 3000:
                    try:
                        self.SE = self.sutter.setVelocity(self.s[0], self.s[1])
                        if self.SE == 0:
                            self.vel = self.s[0]
                            self.res = self.s[1]
                    except:
                        self.SE = 1
                else:
                    self.ui.messagbox.append('Sutter:Please input a velocity less than 3000')
                    self.SE = 1
            elif self.s[1] != self.res and self.s[1] == 1:
                if self.s[0] <= 1310:
                    try:
                        self.SE = self.sutter.setVelocity(self.s[0], self.s[1])
                        if self.SE == 0:
                            self.vel = self.s[0]
                            self.res = self.s[1]
                    except:
                        self.SE = 1
                else:
                    self.ui.messagbox.append('Sutter:Please input a velocity less than 1310')
                    self.SE = 1
            elif (self.s[0] <= 3000 and self.res == 0) or (self.s[0] <= 1310 and self.res == 1):
                try:
                    self.SE = self.sutter.setVelocity(self.s[0], self.res)
                    if self.SE == 0:
                        self.res = self.s[1]
                except:
                    self.SE = 1
            else:
                self.SE = 1
                self.ui.messagbox.append('Sutter:The velocity over the limitation.Please reset')
        if self.s[1] != self.res:
            if self.vel <= 3000 and self.s[1] == 0:
                try:
                    self.SE = self.sutter.setVelocity(self.vel, self.s[1])
                    if self.SE == 0:
                        self.res = self.s[1]
                except:
                    self.SE = 1
            elif self.vel <= 1310 and self.s[1] == 1:
                try:
                    self.SE = self.sutter.setVelocity(self.vel, self.s[1])
                    if self.SE == 0:
                        self.res = self.s[1]
                except:
                    self.SE = 1
            else:
                self.ui.messagbox.append('Sutter:The resolution cannoot match the velocity.Please reset')
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
                self.ui.messagbox.append(act)
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
        self.ui.menuSettings.setEnabled(False)
        pool = QThreadPool.globalInstance()
        # 2. Instantiate the subclass of QRunnable
        runnable = Runnable(3, self.camDisplay)
        # 3. Call start()
        pool.start(runnable)

    def camClose(self):
        # 关闭事件设为触发，关闭视频播放
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
        # 状态判断
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
                # 关闭事件置为未触发，清空显示label
                self.stopEvent.clear()
                break
        self.ui.start.setEnabled(True)
        self.FlagImg = 1
        # if self.FlagRE 需要加保存么
        self.ui.save.setEnabled(True)
        self.ui.menuSettings.setEnabled(True)

    def saveImage(self):  # 保存图片到本地
        if self.FlagImg == 1:
            frame = self.updateImage()
            self.img = frame.copy()
            self.FlagImg = 0
            img1 = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        else:
            img1 = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        fd, type = QFileDialog.getSaveFileName(None, "Save image", "", "*.jpg;;*.png;;All Files(*)")
        img1.save(fd)


def expFileMaxNum(FileName, FolderPath, Layer):
    FolderPath = FolderPath + '/%s' % (Layer)
    Path(FolderPath).mkdir(parents = True, exist_ok = True)
    FileList = glob.glob(FolderPath + '/*')
    if len(FileList) == 0:
        FileCount = 1
    else:
        MaxNum = 0
        for idx in range(len(FileList)):
            temp = re.findall('\d+', FileList[idx])
            temp_list = map(int, temp)
            temp1 = max(temp_list) + 1
            # Find and print the max
            # print(max(num_list))
            if MaxNum < temp1:
                MaxNum = temp1
        FileCount = MaxNum

    DestPath = '%s/%s_%d' % (FolderPath, FileName, FileCount)
    return DestPath


def camRecord():
    fdefault=expFileMaxNum('sperm_sample', './test/', 'test1')
    if MainWindow.cam.IsGrabbing():
        pass
    else:
        MainWindow.camOpen()
    MainWindow.is_running = True
    MainWindow.ui.record.setEnabled(False)
    if not MainWindow.ui.AutoRecord.isChecked():
        fdm= QFileDialog.getSaveFileName(None, "Save Video", "", "*.avi;;All Files(*)")
        if fdm[0]==(''):
            fdm=fdefault
            fd = fdm + '.avi'
        else:
            fd=fdm[0]
    else:
        fd2 = fdefault
        fd=fd2+'.avi'
        tht=threading.Thread(target=AutoStop)
        tht.start()
    thcam = threading.Thread(target = RecordVideo, args = (frame_queue,fd,))
    thcam.start()

def AutoStop():
    t=5
    time.sleep(t)
    if MainWindow.is_running:
        MainWindow.camClose()
    else:
        pass

def RecordVideo(frame,fd):

    fps = 24  # Hz
    time = 30  # seconds
    maxImage = 2400
    if maxImage <= fps * time:
        print('number error ,pass')
        pass
    else:
        writer = get_writer(
            (fd),  # mkv players often support H.264
            fps = fps,  # FPS is in units Hz; should be real-time.
            codec = 'libx264',  # When used properly, this is basically "PNG for video" (i.e. lossless)
            quality = None,  # disables variable compression
            ffmpeg_params = [  # compatibility with older library versions
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
    th1 = threading.Thread(target = MainWindow.setPriorData)
    th1.start()
    th1.join(30)
    th2 = threading.Thread(target = MainWindow.setSutterData)
    th2.start()
    th2.join(30)
    sys.exit(app.exec_())
