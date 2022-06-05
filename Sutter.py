import struct
import time
import serial
from numpy import *


class MP285:

    def __init__(self, com):
        self.timeOut = 5  # timeout in sec
        # self.stepL = 1
        self.stepMult = 400
        self.port = 'COM'+str(com)
        try:
            self.ser = serial.Serial(port = self.port, baudrate = 9600, bytesize = serial.EIGHTBITS,
                                     parity = serial.PARITY_NONE,
                                     stopbits = serial.STOPBITS_ONE, timeout = self.timeOut)
        except Exception as ex:
            print("open serial port error " + str(ex))
            # sys.exit (1)
        self.updatePanel()
        self.exitFlag = 0

    # destructor
    def __del__(self):
        self.ser.close()
        print('sutter close')

    # info getting
    def updatePanel(self):
        self.ser.flushInput()  # flush input buffer
        self.ser.flushOutput()  # flush output buffer
        self.ser.write(b'n\r')  # Sutter replies with a CR
        time.sleep(0.2)

    def getPosition(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            # write 8 byte data
            self.ser.write(b'c\r')
            xyzb = self.ser.read(13)
            # TODO bytes to str
            xyz_um = array(struct.unpack('lll', xyzb[:12])) * 0.04
            time.sleep(0.2)
            return xyz_um
        except:
            time.sleep(0.2)

    # settings
    def getStatus(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            self.ser.write(b's\r')  # send status command
            r = self.ser.read(33)
            self.stepMult = double(r[25]) * 256 + double(r[24])
            self.currentVelocity = double(127 & r[29]) * 256 + double(r[28])
            return self.stepMult, self.currentVelocity
        except:
            return 'Sutter fail to get status'

    def setOrignal(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            self.ser.write(b'o\r')
            time.sleep(0.2)
            return 0
        except:
            return 1

    def setVelocity(self, vel, res):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            ResV = struct.pack('H', int(vel) + ((res) * 2 ** 15))
            self.ser.write(b'V' + ResV + b'\r')
            time.sleep(0.2)
            return 0
        except:
            return 1

    # def reset(self):
    #     try:
    #         self.ser.flushInput()  # flush input buffer
    #         self.ser.flushOutput()  # flush output buffer
    #         self.ser.write(b'r\r')
    #         r=self.ser.read(1)
    #         print(r)
    #     except:
    #         print("reset sutter error")
    #         time.sleep(0.2)

    # movement functions

    def goForward(self, n):
        try:
            # self.ser.flushInput()  # flush input buffer
            # self.ser.flushOutput()  # flush output buffer
            # self.ser.write(b'c\r')
            # xyzb = self.ser.read(13)
            pos = self.getPosition()
            #读出当前坐标,step to micron
            xyz_m = struct.pack('lll', int(pos[0] * 10000 / self.stepMult),
                                int((pos[1] + n) * 10000 / self.stepMult),
                                int(pos[2] * 10000 / self.stepMult))
            #input coordinate from miron to step
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyz_m + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter move forward completed in (%.2f sec)' % (endt - startt)
        except:
            return 'Sutter fail to move forward'

    def goBack(self, n):
        try:
            # self.ser.flushInput()  # flush input buffer
            # self.ser.flushOutput()  # flush output buffer
            # self.ser.write(b'c\r')
            # xyzb = self.ser.read(13)
            pos = self.getPosition()
            # pos = array(struct.unpack('lll', xyzb[:12])) * self.stepMult / 10000
            #读出当前坐标,step to micron
            xyz_m = struct.pack('lll', int(pos[0] * 10000 / self.stepMult),
                                int((pos[1] - n) * 10000 / self.stepMult),
                                int(pos[2] * 10000 / self.stepMult))
            #input coordinate from miron to step
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyz_m + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter move back completed in (%.2f sec)' % (endt - startt)
        except:
            return 'Sutter fail to move back'

    def goLeft(self, n):
        try:
            # self.ser.flushInput()  # flush input buffer
            # self.ser.flushOutput()  # flush output buffer
            # self.ser.write(b'c\r')
            # xyzb = self.ser.read(13)
            # pos = array(struct.unpack('lll', xyzb[:12])) * self.stepMult / 10000
            pos = self.getPosition()
            #读出当前坐标,step to micron
            xyz_m = struct.pack('lll', int((pos[0] - n) * 10000 / self.stepMult),
                                int(pos[1] * 10000 / self.stepMult),
                                int(pos[2] * 10000 / self.stepMult))
            #input coordinate from miron to step
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyz_m + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter move left completed in (%.2f sec)' % (endt - startt)
        except:
            return 'Sutter fail to move left'

    def goRight(self, n):
        try:
            # self.ser.flushInput()  # flush input buffer
            # self.ser.flushOutput()  # flush output buffer
            # self.ser.write(b'c\r')
            # xyzb = self.ser.read(13)
            # pos = array(struct.unpack('lll', xyzb[:12])) * self.stepMult / 10000
            pos = self.getPosition()
            #读出当前坐标,step to micron
            xyz_m = struct.pack('lll', int((pos[0] + n) * 10000 / self.stepMult), int(pos[1] * 10000 / self.stepMult),
                                int(pos[2] * 10000 / self.stepMult))
            #input coordinate from miron to step
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyz_m + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter move right completed in (%.2f sec)' % (endt - startt)
        except:
            return "Sutter fail to move right"

    def goUp(self, n):
        try:
            # self.ser.flushInput()  # flush input buffer
            # self.ser.flushOutput()  # flush output buffer
            # self.ser.write(b'c\r')
            # xyzb = self.ser.read(13)
            # pos = array(struct.unpack('lll', xyzb[:12])) * 0.04
            pos = self.getPosition()
            # 读出当前坐标,step to micron
            xyz_m = struct.pack('lll', int(pos[0] * 10000 / self.stepMult),
                                int(pos[1] * 10000 / self.stepMult), int((pos[2] + n) * 10000 / self.stepMult))
            # input coordinate from miron to step
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyz_m + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter move up completed in (%.2f sec)' % (endt - startt)
        except:
            return "Sutter fail to move up"

    def goDown(self, n):
        try:
            # self.ser.flushInput()  # flush input buffer
            # self.ser.flushOutput()  # flush output buffer
            # self.ser.write(b'c\r')
            # xyzb = self.ser.read(13)
            # pos = array(struct.unpack('lll', xyzb[:12])) * self.stepMult / 10000
            pos = self.getPosition()
            # 读出当前坐标,step to micron
            xyz_m = struct.pack('lll', int(pos[0] * 10000 / self.stepMult),
                                int(pos[1] * 10000 / self.stepMult), int((pos[2] - n) * 10000 / self.stepMult))
            # input coordinate from miron to step
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyz_m + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter move down completed in (%.2f sec)' % (endt - startt)
        except:
            return "Sutter fail to move down"

    def goHome(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            xyzb = struct.pack('lll', int(0), int(0), int(0))  # convert integer values into bytes
            startt = time.time()  # start timer
            self.ser.write(
                b'm' + xyzb + b'\r')  # send position to controller; add the "m" and the CR to create the move command
            cr = []
            cr = self.ser.read(1)  # read carriage return and ignore
            endt = time.time()  # stop timer
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut, 1
            else:
                return 'Sutter go home completed in (%.2f sec)' % (endt - startt), 0
        except:
            return 'Sutter fail to go home', 1

    def gotoPosition(self, pos = []):
        if len(pos) != 3:
            print('Length of position argument has to be three')
            sys.exit(1)
        self.ser.flushInput()  # flush input buffer
        self.ser.flushOutput()  # flush output buffer
        xyzb = struct.pack('lll', int(pos[0] * 10000 / self.stepMult), int(pos[1] * 10000 / self.stepMult),
                           int(pos[2] * 10000 / self.stepMult))  # convert integer values into bytes
        startt = time.time()  # start timer
        self.ser.write(
            b'm' + xyzb + b'\r')  # send position to controller; add the "m" and the CR to create the move command
        cr = []
        cr = self.ser.read(1)  # read carriage return and ignore
        endt = time.time()  # stop timer
        time.sleep(0.2)
        if len(cr) == 0:
            return 'Sutter did not finish moving before timeout (%d sec).' % self.timeOut
        else:
            return 'sutterMP285: Sutter move completed in (%.2f sec)' % (endt - startt)

    def interrupt(self):
        try:
            self.ser.flushInput()  # flush input buffer
            self.ser.flushOutput()  # flush output buffer
            i = bin(3).encode()
            self.ser.write(i)
            cr = self.ser.read(1)
            time.sleep(0.2)
            if len(cr) == 0:
                return 'Sutter did not stop before timeout (%d sec).' % self.timeOut
            else:
                return 'Sutter stop '
        except:
            return 'Sutter fail to stop'

    #TODO setting ErrorS
