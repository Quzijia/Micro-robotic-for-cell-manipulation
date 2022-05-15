import time
import serial
from numpy import *
import re


class Prior:
    def __init__(self):
        self.exitFlag = 0
        self.timeOut = 0.5  # timeout in sec
        self.errorF = 0
        self.processF = 0
        # initialize serial connection to controller
        try:
            self.ser = serial.Serial(port = 'COM3', baudrate = 9600, bytesize = serial.EIGHTBITS,
                                     parity = serial.PARITY_NONE,
                                     stopbits = serial.STOPBITS_ONE, timeout = self.timeOut)
        except Exception as ex:
            print("open serial port error " + str(ex))
        self.comp=str(0).encode()
        self.ser.write(b'comp\t'+self.comp+b'\r\n')
        self.error = str(0).encode()
        self.ser.write(b'ERROR\t' + self.error + b'\r\n')
        # report the error to human，Readable text

    def reTranslate(self, r, arg):
        if arg == 2:
            u = re.findall(r"(\d+),", r)
            v = re.findall(r"(?<=\,)\d+", r)
            u1 = list(map(int, u))
            v1 = list(map(int, v))
            u2 = u1[0]
            v2 = v1[0]
            return u2, v2
        else:
            pass

    def errorFind(self, r):
        pass

    # get&set
    def setStep(self, u, v):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            u1 = str(u).encode()
            v1 = str(v).encode()
            self.ser.write(b'x\r\n')
            self.ser.write(b'X\t' + u1 + b'\t' + v1 + b'\r\n')
            response = self.ser.read(8)
            self.errorFind(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getStep(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            self.ser.write(b'x\r\n')
            response = self.ser.read(40)
            r = (response).decode()
            try:
                (a, b) = self.reTranslate(r, 2)
                return(a, b)
            except:
                return (r)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def setMicroStep(self, s):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            s1 = str(s).encode()
            self.ser.write(b'ss\t' + s1 + b'\r\n')
            # response = self.ser.read(4)
            # self.errorFind(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getMicroStep(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'SS\r\n')
            response = self.ser.read(8)
            self.reTranslate(response)
            #     TODO change to a return
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def getAbPos(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'p\r\n')
            response = self.ser.read(16)
            print(response)
            #     TODO 后期应该是return
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def setAcceleration(self, n):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            n1 = str(n).encode()
            self.ser.write(b'SAS\t' + n1 + b'\tu\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def setMaxAcceleration(self, a):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            a1 = str(a).encode()
            self.ser.write(b'SAS\t' + a1 + b'\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getAcceleration(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'SAS\tu\r\n')
            response = self.ser.read(8)
            print(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def setCurve(self, c):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            c1 = str(c).encode()
            self.ser.write(b'SCS\t' + c1 + b'\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getCurve(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'SCS\r\n')
            response = self.ser.read(8)
            print(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def setMaxSpeed(self, m):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            m1 = str(m).encode()
            self.ser.write(b'SMS' + m1 + b'\r\n')
            response = self.ser.read(4)
            print(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def getMaxSpeed(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'SMS\r\n')
            response = self.ser.read(8)
            print(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def setSpeed(self, n):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            n1 = str(n).encode()
            self.ser.write(b'SMS\t' + n1 + b'u\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getSpeed(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'SMS\tu\r\n')
            response = self.ser.read(4)
            print(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            pass

    def hostXreverse(self, d):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            d1 = str(d).encode()
            self.ser.write(b'XD\t' + d1 + b'\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def hostYreverse(self, d):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            d1 = str(d).encode()
            self.ser.write(b'YD\t' + d1 + b'\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def encoderEnable(self, b):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            d1 = str(b).encode()
            self.ser.write(b'YD\t' + d1 + b'\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getHostBackLash(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'BLSH\r\n')
            response = self.ser.read(8)
            print(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Please check the connection'

    def HostBackLashEnable(self, s, b):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            s1 = str(s).encode()
            # write 8 byte data
            if s == 1:
                b1 = str(b).encode()
                self.ser.write(b'BLSH\t' + s1 + b'\t' + b1 + b'\r\n')
            elif s == 0:
                self.ser.write(b'BLSH\t' + s1 + b'\r\n')
            # response = self.ser.read(8)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    # functions of movements
    def moveStop(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'I\r\n')
            time.sleep(0.1)  # wait 0.1s
            return 'Prior stop completed'
        except:
            return'Prior fail to stop'

    def suddenStop(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'K\r\n')
            return 'Prior sudden stop completed'
        except:
            return'Prior fail to sudden stop'

    def goHome(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'm\r\n')
            time.sleep(0.1)  # wait 0.1s
            return'Prior go home completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return'Prior fail to go home'

    def goAbPos(self, x, y):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            x1 = str(x).encode()
            y1 = str(y).encode()
            self.ser.write(b'g\t' + x1 + b'\t' + y1 + b'\r\n')
            time.sleep(0.1)  # wait 0.1s
            return'Prior move completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return 'Prior fail to move'

    def goAbPosX(self, x):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            x1 = str(x).encode()
            self.ser.write(b'gx\t' + x1 + b'\r\n')
            time.sleep(0.1)  # wait 0.1s
            return'Prior move completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return 'Prior fail to move'

    def goAbPosY(self, y):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            y1 = str(y).encode()
            self.ser.write(b'gy\t' + y1 + b'\r\n')
            time.sleep(0.1)  # wait 0.1s
            return 'Prior move completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return 'Prior fail to move'

    def goRePos(self, x, y):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            x1 = str(x).encode()
            y1 = str(y).encode()
            self.ser.write(b'gr\t' + x1 + b'\t' + y1 + b'\r\n')
            time.sleep(0.1)  # wait 0.1s
            return 'Prior move completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return 'Prior fail to move'

    def moveLeft(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'l\r\n')
            time.sleep(0.1)  # wait 0.1s
            return 'Prior move left completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return'Prior fail to move left'

    def moveRight(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'r\r\n')
            time.sleep(0.1)  # wait 0.1s
            return'Prior move right completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return'Prior fail to move right'

    def moveForward(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'f\r\n')
            time.sleep(0.1)  # wait 0.1s
            return 'Prior move forward completed'
        except:
            time.sleep(0.1)  # wait 0.1s
            return'Prior fail to move forward'

    def moveBack(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'b\r\n')
            time.sleep(0.1)  # wait 0.1s
            return'Prior move back completed'
        except:

            return 'Prior fail to move back'

    # joystick settings
    def joystickSetEnable(self, flag):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            if flag == 1:
                self.ser.write(b'j\r\n')
            elif flag == 0:
                self.ser.write(b'h\r\n')
                time.sleep(0.1)  # wait 0.1s
                return 0
        except:
            return 1

    def setJoystickSpeed(self, s):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            s1 = str(s).encode()
            self.ser.write(b'o\t' + s1 + b'%\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def getJoystickSpeed(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'o\r\n')
            response = self.ser.read(4)
            time.sleep(0.1)
            return response
        except:
            time.sleep(0.1)  # wait 0.1s
            return 'Prior fail to get joystick speed'

    def joystickXreverse(self, d):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            d1 = str(d).encode()
            self.ser.write(b'JXD\t' + d1 + b'\r\n')
            # response = self.ser.read(4)
            # return(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def joystickYreverse(self, d):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            d1 = str(d).encode()
            self.ser.write(b'JYD\t' + d1 + b'\r\n')
            # response = self.ser.read(4)
            # print(response)
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    # stage mapping
    def getCorrection(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            self.ser.write(b'CORRECT\r\n')
            response = self.ser.read(8)
            return (response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return 'Prior fail to get correction state'
            pass

    def getCorrection4pt(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            self.ser.write(b'CORRECT\t?\r\n')
            response = self.ser.read(20)
            return(response)
            time.sleep(0.1)  # wait 0.1s
        except:
            return'Prior fail to get correction points'

    def correctionEnable(self, f):
        if f == 0:
            r = b'D'
        elif f == 1:
            r = b'E'
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            self.ser.write(b'CORRECT\t' + r + b'\r\n')
            time.sleep(0.1)  # wait 0.1s
            return 0
        except:
            return 1

    def __del__(self):
        self.ser.close()
        print('prior close')
