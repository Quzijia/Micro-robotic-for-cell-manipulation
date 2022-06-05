from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from PyQt5.QtWidgets import QDialog
from SubUI.subui import Ui_Dialog,Ui_Dialog2,Ui_Dialog3,Ui_Dialog4


class BaslerWindow(QDialog):
    def __init__(self):
        super(BaslerWindow, self).__init__()
        self.sub = Ui_Dialog3()
        self.sub.setupUi(self)
        self.process2 = Worksignal()

    def accept(self):
        rt = self.sub.spinBox_2.value()
        self.process2.currentReTime.emit(rt)
        self.close()


class DevicesWindow(QDialog):
    def __init__(self):
        super(DevicesWindow, self).__init__()
        self.sub = Ui_Dialog4()
        self.sub.setupUi(self)


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
        s = self.sub.speed.value()
        a = self.sub.acceleteation.value()
        c = self.sub.curve.value()
        stage = [s, a, c]
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
        ms = self.sub.microStep.value()
        if self.sub.encoderEnable.isChecked():
            ee = 1
        else:
            ee = 0
        other = [ms, ee]
        n = self.sub.xFields.value()
        m = self.sub.yFields.value()
        t = self.sub.timeInter.value()
        r = self.sub.repeat.value()
        pattern = [n, m, t, r]
        self.process1.currentPrior.emit((default, stage, joy, other, pattern))
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
    currentReTime = pyqtSignal(object)

class Runnable(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Runnable, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)