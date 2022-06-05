class paramas:
    def __init__(self):
        super(paramas, self).__init__()
    def paramaSetting(self):
        self.FlagP = 0
        # Prior exit code
        self.FlagS = 0
        # Sutter exit code
        self.FlagImg = 0
        self.FlagP = 1
        self.priorStepSizeX = 500
        self.priorStepSizeY = 500
        self.prior4pC = 1
        self.priorHBL = 1
        self.priorHBLD = 100
        self.priorSpeed = 600
        self.priorAcce = 20000
        self.priorCurve = 100
        self.priorJoystickSpeed = 100
        self.priorjoystickEnable = 1
        self.priorEncoderEnable = 1
        self.priorJX = 1
        self.priorJY = 1
        self.priorXD = 1
        self.priorYD = 1
        self.priorMicroStep = 100
        self.priorXfields = 4
        self.priorYfields = 4
        self.priorTimeInter = 1
        self.priorRepeat = 0
        self.recordTime = 5
        self.stopPrior = 0
        return self.FlagP,self.FlagS,self.FlagImg,self.FlagP,self.priorStepSizeX, self.priorStepSizeY,self.prior4pC,self.priorHBL,self.priorHBLD,self.priorSpeed,self.priorAcce,self.priorCurve,self.priorJoystickSpeed, self.priorjoystickEnable,self.priorEncoderEnable,self.priorJX,self.priorJY,self.priorXD,self.priorYD,self.priorMicroStep,self.priorXfields,self.priorYfields,self.priorTimeInter,self.priorRepeat,self.recordTime,self.stopPrior
