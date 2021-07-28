# coding: utf-8
# Driver for D7S.

import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice



print("board", dir(board))

class GroveD7s:
    I2C_ADDR = 0x55

    REG_STATE           = b'\x10\x00'
    REG_AXIS_STATE      = b'\x10\x01'
    REG_EVENT           = b'\x10\x02'
    REG_MODE            = b'\x10\x03'
    REG_CTRL            = b'\x10\x04'
    REG_CLEAR_COMMAND   = b'\x10\x05'

    # Values for REG_STATE registers
    STATUS_NORMAL_MODE                  = b'\x00'
    STATUS_NORMAL_MODE_NOT_IN_STANBY    = b'\x01'
    STATUS_INITIAL_INSTALLATION_MODE    = b'\x02'
    STATUS_OFFSET_ACQUISITION_MODE      = b'\x03'
    STATUS_SELFTEST_MODE                = b'\x04'

    # REG_MODE
    NORMAL_MODE                  = b'\x01'
    INITIAL_INSTALLATION_MODE    = b'\x02'
    OFFSET_ACQUISITION_MODE      = b'\x03'
    SELFTEST_MODE                = b'\x04'

    #Event
    EVENT_SHUT = b'\x08'
    EVENT_COLLAPSE = b'\x04'
    EVENT_SELFTEST = b'\x02'
    EVENT_OFFSET = b'\x01'

    # Axis states
    AXIS_YZ    = b'\x00'
    AXIS_XZ    = b'\x01'
    AXIS_XY    = b'\x02'

    REG_MAIN_SI_H       = b'\x20\x00'
    REG_MAIN_SI_L       = b'\x20\x01'
    REG_PGA_H           = b'\x20\x02'
    REG_PGA_L           = b'\x20\x03'

    # Latest Data 1
    REG_N1_MAIN_X_H        = b'\x30\x00'
    REG_N1_MAIN_X_L        = b'\x30\x01'
    REG_N5_MAIN_Y_H        = b'\x30\x02'
    REG_N5_MAIN_Y_L        = b'\x30\x03'
    REG_N5_MAIN_Z_H        = b'\x30\x04'
    REG_N5_MAIN_Z_L        = b'\x30\x05'
    REG_N1_MAIN_T_AVE_H    = b'\x30\x06'
    REG_N1_MAIN_T_AVE_L    = b'\x30\x07'
    REG_N1_MAIN_SI_H       = b'\x30\x08'
    REG_N1_MAIN_SI_L       = b'\x30\x09'
    REG_N1_PGA_H           = b'\x30\x0A'
    REG_N1_PGA_L           = b'\x30\x0B'

    # Latest Data 2
    REG_N2_MAIN_X_H        = b'\x31\x00'
    REG_N2_MAIN_X_L        = b'\x31\x01'
    REG_N2_MAIN_Y_H        = b'\x31\x02'
    REG_N2_MAIN_Y_L        = b'\x31\x03'
    REG_N2_MAIN_Z_H        = b'\x31\x04'
    REG_N2_MAIN_Z_L        = b'\x31\x05'
    REG_N2_MAIN_T_AVE_H    = b'\x31\x06'
    REG_N2_MAIN_T_AVE_L    = b'\x31\x07'
    REG_N2_MAIN_SI_H       = b'\x31\x08'
    REG_N2_MAIN_SI_L       = b'\x31\x09'
    REG_N2_PGA_H           = b'\x31\x0A'
    REG_N2_PGA_L           = b'\x31\x0B'

    # Latest Data 3
    REG_N3_MAIN_X_H        = b'\x32\x00'
    REG_N3_MAIN_X_L        = b'\x32\x01'
    REG_N3_MAIN_Y_H        = b'\x32\x02'
    REG_N3_MAIN_Y_L        = b'\x32\x03'
    REG_N3_MAIN_Z_H        = b'\x32\x04'
    REG_N3_MAIN_Z_L        = b'\x32\x05'
    REG_N3_MAIN_T_AVE_H    = b'\x32\x06'
    REG_N3_MAIN_T_AVE_L    = b'\x32\x07'
    REG_N3_MAIN_SI_H       = b'\x32\x08'
    REG_N3_MAIN_SI_L       = b'\x32\x09'
    REG_N3_PGA_H           = b'\x32\x0A'
    REG_N3_PGA_L           = b'\x32\x0B'

    # Latest Data 4
    REG_N4_MAIN_X_H        = b'\x33\x00'
    REG_N4_MAIN_X_L        = b'\x33\x01'
    REG_N4_MAIN_Y_H        = b'\x33\x02'
    REG_N4_MAIN_Y_L        = b'\x33\x03'
    REG_N4_MAIN_Z_H        = b'\x33\x04'
    REG_N4_MAIN_Z_L        = b'\x33\x05'
    REG_N4_MAIN_T_AVE_H    = b'\x33\x06'
    REG_N4_MAIN_T_AVE_L    = b'\x33\x07'
    REG_N4_MAIN_SI_H       = b'\x33\x08'
    REG_N4_MAIN_SI_L       = b'\x33\x09'
    REG_N4_PGA_H           = b'\x33\x0A'
    REG_N4_PGA_L           = b'\x33\x0B'

    # latest Data 5
    REG_N5_MAIN_X_H        = b'\x34\x00'
    REG_N5_MAIN_X_L        = b'\x34\x01'
    REG_N5_MAIN_Y_H        = b'\x34\x02'
    REG_N5_MAIN_Y_L        = b'\x34\x03'
    REG_N5_MAIN_Z_H        = b'\x34\x04'
    REG_N5_MAIN_Z_L        = b'\x34\x05'
    REG_N5_MAIN_T_AVE_H    = b'\x34\x06'
    REG_N5_MAIN_T_AVE_L    = b'\x34\x07'
    REG_N5_MAIN_SI_H       = b'\x34\x08'
    REG_N5_MAIN_SI_L       = b'\x34\x09'
    REG_N5_PGA_H           = b'\x34\x0A'
    REG_N5_PGA_L           = b'\x34\x0B'



    # SI Ranked Data 1
    REG_M1_MAIN_X_H        = b'\x35\x00'
    REG_M1_MAIN_X_L        = b'\x35\x01'
    REG_M5_MAIN_Y_H        = b'\x35\x02'
    REG_M5_MAIN_Y_L        = b'\x35\x03'
    REG_M5_MAIN_Z_H        = b'\x35\x04'
    REG_M5_MAIN_Z_L        = b'\x35\x05'
    REG_M1_MAIN_T_AVE_H    = b'\x35\x06'
    REG_M1_MAIN_T_AVE_L    = b'\x35\x07'
    REG_M1_MAIN_SI_H       = b'\x35\x08'
    REG_M1_MAIN_SI_L       = b'\x35\x09'
    REG_M1_PGA_H           = b'\x35\x0A'
    REG_M1_PGA_L           = b'\x35\x0B'

    # SI Ranked Data 2
    REG_M2_MAIN_X_H        = b'\x36\x00'
    REG_M2_MAIN_X_L        = b'\x36\x01'
    REG_M2_MAIN_Y_H        = b'\x36\x02'
    REG_M2_MAIN_Y_L        = b'\x36\x03'
    REG_M2_MAIN_Z_H        = b'\x36\x04'
    REG_M2_MAIN_Z_L        = b'\x36\x05'
    REG_M2_MAIN_T_AVE_H    = b'\x36\x06'
    REG_M2_MAIN_T_AVE_L    = b'\x36\x07'
    REG_M2_MAIN_SI_H       = b'\x36\x08'
    REG_M2_MAIN_SI_L       = b'\x36\x09'
    REG_M2_PGA_H           = b'\x36\x0A'
    REG_M2_PGA_L           = b'\x36\x0B'

    # SI Ranked Data 3
    REG_M3_MAIN_X_H        = b'\x37\x00'
    REG_M3_MAIN_X_L        = b'\x37\x01'
    REG_M3_MAIN_Y_H        = b'\x37\x02'
    REG_M3_MAIN_Y_L        = b'\x37\x03'
    REG_M3_MAIN_Z_H        = b'\x37\x04'
    REG_M3_MAIN_Z_L        = b'\x37\x05'
    REG_M3_MAIN_T_AVE_H    = b'\x37\x06'
    REG_M3_MAIN_T_AVE_L    = b'\x37\x07'
    REG_M3_MAIN_SI_H       = b'\x37\x08'
    REG_M3_MAIN_SI_L       = b'\x37\x09'
    REG_M3_PGA_H           = b'\x37\x0A'
    REG_M3_PGA_L           = b'\x37\x0B'

    # SI Ranked Data 4
    REG_M4_MAIN_X_H        = b'\x38\x00'
    REG_M4_MAIN_X_L        = b'\x38\x01'
    REG_M4_MAIN_Y_H        = b'\x38\x02'
    REG_M4_MAIN_Y_L        = b'\x38\x03'
    REG_M4_MAIN_Z_H        = b'\x38\x04'
    REG_M4_MAIN_Z_L        = b'\x38\x05'
    REG_M4_MAIN_T_AVE_H    = b'\x38\x06'
    REG_M4_MAIN_T_AVE_L    = b'\x38\x07'
    REG_M4_MAIN_SI_H       = b'\x38\x08'
    REG_M4_MAIN_SI_L       = b'\x38\x09'
    REG_M4_PGA_H           = b'\x38\x0A'
    REG_M4_PGA_L           = b'\x38\x0B'

    # latest Data 5
    REG_M5_MAIN_X_H        = b'\x39\x00'
    REG_M5_MAIN_X_L        = b'\x39\x01'
    REG_M5_MAIN_Y_H        = b'\x39\x02'
    REG_M5_MAIN_Y_L        = b'\x39\x03'
    REG_M5_MAIN_Z_H        = b'\x39\x04'
    REG_M5_MAIN_Z_L        = b'\x39\x05'
    REG_M5_MAIN_T_AVE_H    = b'\x39\x06'
    REG_M5_MAIN_T_AVE_L    = b'\x39\x07'
    REG_M5_MAIN_SI_H       = b'\x39\x08'
    REG_M5_MAIN_SI_L       = b'\x39\x09'
    REG_M5_PGA_H           = b'\x39\x0A'
    REG_M5_PGA_L           = b'\x39\x0B'




    #
    # Initial installation Data
    OFFSET_SET_X_H            = b'\x40\x00'
    OFFSET_SET_X_L            = b'\x40\x01'
    OFFSET_SET_Y_H            = b'\x40\x02'
    OFFSET_SET_Y_L            = b'\x40\x03'
    OFFSET_SET_Z_H            = b'\x40\x04'
    OFFSET_SET_Z_L            = b'\x40\x05'
    OFFSET_SET_T_AVE_H        = b'\x40\x06'
    OFFSET_SET_T_AVE_L        = b'\x40\x07'
    OFFSET_SET_MAX_X_H        = b'\x40\x08'
    OFFSET_SET_MAX_X_L        = b'\x40\x09'
    OFFSET_SET_MAX_Y_H        = b'\x40\x0A'
    OFFSET_SET_MAX_Y_L        = b'\x40\x0B'
    OFFSET_SET_MAX_Z_H        = b'\x40\x0C'
    OFFSET_SET_MAX_Z_L        = b'\x40\x0D'
    OFFSET_SET_MIN_X_H        = b'\x40\x0E'
    OFFSET_SET_MIN_X_L        = b'\x40\x0F'
    OFFSET_SET_MIN_Y_H        = b'\x40\x10'
    OFFSET_SET_MIN_Y_L        = b'\x40\x11'
    OFFSET_SET_MIN_Z_H        = b'\x40\x12'
    OFFSET_SET_MIN_Z_L        = b'\x40\x13'
    OFFSET_SET_AXIS           = b'\x40\x14'

    #
    # SI Ranked Offset Data'
    OFFSET_RECENT_X_H            = b'\x41\x00'
    OFFSET_RECENT_X_L            = b'\x41\x01'
    OFFSET_RECENT_Y_H            = b'\x41\x02'
    OFFSET_RECENT_Y_L            = b'\x41\x03'
    OFFSET_RECENT_Z_H            = b'\x41\x04'
    OFFSET_RECENT_Z_L            = b'\x41\x05'
    OFFSET_RECENT_T_AVE_H        = b'\x41\x06'
    OFFSET_RECENT_T_AVE_L        = b'\x41\x07'
    OFFSET_RECENT_MAX_X_H        = b'\x41\x08'
    OFFSET_RECENT_MAX_X_L        = b'\x41\x09'
    OFFSET_RECENT_MAX_Y_H        = b'\x41\x0A'
    OFFSET_RECENT_MAX_Y_L        = b'\x41\x0B'
    OFFSET_RECENT_MAX_Z_H        = b'\x41\x0C'
    OFFSET_RECENT_MAX_Z_L        = b'\x41\x0D'
    OFFSET_RECENT_MIN_X_H        = b'\x41\x0E'
    OFFSET_RECENT_MIN_X_L        = b'\x41\x0F'
    OFFSET_RECENT_MIN_Y_H        = b'\x41\x10'
    OFFSET_RECENT_MIN_Y_L        = b'\x41\x11'
    OFFSET_RECENT_MIN_Z_H        = b'\x41\x12'
    OFFSET_RECENT_MIN_Z_L        = b'\x41\x13'
    OFFSET_RECENT_RECENT_STATE   = b'\x41\x14'

    #
    # Self-Diagnotic Data'
    SELFTEST_BEFORE_X_H    = b'\x42\x00'
    SELFTEST_BEFORE_X_L    = b'\x42\x01'
    SELFTEST_AFTER_X_H     = b'\x42\x02'
    SELFTEST_AFTER_X_L     = b'\x42\x03'
    SELFTEST_BEFORE_Y_H    = b'\x42\x04'
    SELFTEST_BEFORE_Y_L    = b'\x42\x05'
    SELFTEST_AFTER_Y_H     = b'\x42\x06'
    SELFTEST_AFTER_Y_L     = b'\x42\x07'
    SELFTEST_BEFORE_Z_H    = b'\x42\x08'
    SELFTEST_BEFORE_Z_L    = b'\x42\x09'
    SELFTEST_AFTER_Z_H     = b'\x42\x0A'
    SELFTEST_AFTER_Z_L     = b'\x42\x0B'
    SELFTEST_T_AVE_H       = b'\x42\x0C'
    SELFTEST_T_AVE_L       = b'\x42\x0D'
    SELFTEST_ERROR         = b'\x42\x0E'

    def __init__(self, dodiag=False):
        self.I2C_ADDR = 0x55

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.i2c.try_lock()
        print(self.i2c.scan())
        self.i2c.unlock()
        self.device = I2CDevice(self.i2c, self.I2C_ADDR)
        print(dir(self.device))

        print("0 Current mode:", self.readByte(self.REG_MODE))

        #self.writeByte(self.REG_MODE, b'\x00')
        #time.sleep(2.0)


        if dodiag:
            print("DIAG")
            self.writeByte(self.REG_MODE, b'\x04')
        else:
            print("REG")
            self.writeByte(self.REG_MODE, b'\x02')

        time.sleep(2.0)
        print("1 Current mode:", self.readByte(self.REG_MODE))

        print("1 Current state:", self.readByte(self.REG_STATE))
        self.writeByte(self.REG_CTRL, b'\x04')
        time.sleep(2.0)

    def setState(self, mode):
        if mode < b'\x01' or mode > b'\x04' :
            print("Invalid value:", mode)
            return


    def getState(self):
        status = self.readByte(self.REG_STATE)
        return status

    def getMode(self):
        status = self.readByte(self.REG_Mode)
        return status


    def getEvent(self):
        status = self.readByte(self.REG_EVENT)
        return status

    def isReady(self):
        try:
            state = self.getState()
            return self.getState() == self.STATUS_NORMAL_MODE
        except OSError:
            print('OSError')
            return False

    def isEarthquakeOccuring(self):
        return self.getState() == self.STATUS_NORMAL_MODE_NOT_IN_STANBY

    def getInstantaneusSI(self):
        si = self.readByte16(self.REG_MAIN_SI_H)
        if si != None:
            si /= 1
        return si

    def getInstantaneusPGA(self):
        pga = self.readByte16(self.REG_PGA_H)
        return pga

    #
    # I2C IO Functions
    #
    def readByte(self, register16):

        try:
            with self.device:
                self.device.write(register16)
                data = bytearray(1)
                self.device.readinto(data)
            return data
        except OSError:
            return None

    def readByte16(self, register16):
        datah = self.readByte(register16)
        datal = self.readByte(register16+1)

        print('r16', datah, datal)
        if datah is not None and datal is not None:
            return (datah[0] << 8) | (datal[0] & 0xFF)
        return None

    def writeByte(self, register16, data):

        buf = register16 + data
        print('BUF', buf)
        print('buf type', type(buf))

        with self.device:
            self.device.write(buf)

    def writeByte16(self, register16, data16):
        buf = register16.to_bytes(2, 'big')
        buf += data.to_bytes(2, 'big')
        with self.device:
            self.device.write(buf)

