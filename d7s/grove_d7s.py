# coding: utf-8
# Driver for D7S.

#import smbus
#import RPi.GPIO as GPIO
import time
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_bus_device.i2c_device import I2CDevice


print("i2c", dir(i2c))
print("board", dir(board))

class GroveD7s:
    I2C_ADDR = 0x55

    REG_STATE           = 0x1000
    REG_AXIS_STATE      = 0x1001
    REG_EVENT           = 0x1002
    REG_MODE            = 0x1003
    REG_CTRL            = 0x1004
    REG_CLEAR_COMMAND   = 0x1005

    REG_MAIN_SI_H       = 0x2000
    REG_MAIN_SI_L       = 0x2001
    REG_PGA_H           = 0x2002
    REG_PGA_L           = 0x2003

    REG_N1_MAIN_T_AVE_H       = 0x3006
    REG_N1_MAIN_T_AVE_L       = 0x3007
    REG_N1_MAIN_SI_H       = 0x3008
    REG_N1_MAIN_SI_L       = 0x3009
    REG_N1_PGA_H           = 0x300A
    REG_N1_PGA_L           = 0x300B

    REG_N2_MAIN_T_AVE_H       = 0x3006
    REG_N2_MAIN_T_AVE_L       = 0x3007
    REG_N2_MAIN_SI_H       = 0x3008
    REG_N2_MAIN_SI_L       = 0x3009
    REG_N2_PGA_H           = 0x300A
    REG_N2_PGA_L           = 0x300B

    REG_N3_MAIN_T_AVE_H       = 0x3006
    REG_N3_MAIN_T_AVE_L       = 0x3007
    REG_N3_MAIN_SI_H       = 0x3008
    REG_N3_MAIN_SI_L       = 0x3009
    REG_N3_PGA_H           = 0x300A
    REG_N3_PGA_L           = 0x300B

    REG_N4_MAIN_T_AVE_H       = 0x3006
    REG_N4_MAIN_T_AVE_L       = 0x3007
    REG_N4_MAIN_SI_H       = 0x3008
    REG_N4_MAIN_SI_L       = 0x3009
    REG_N4_PGA_H           = 0x300A
    REG_N4_PGA_L           = 0x300B

    REG_N5_MAIN_T_AVE_H       = 0x3006
    REG_N5_MAIN_T_AVE_L       = 0x3007
    REG_N5_MAIN_SI_H       = 0x3008
    REG_N5_MAIN_SI_L       = 0x3009
    REG_N5_PGA_H           = 0x300A
    REG_N5_PGA_L           = 0x300B

    STATUS_NORMAL_MODE                  = 0x00
    STATUS_NORMAL_MODE_NOT_IN_STANBY    = 0x01
    STATUS_INITIAL_INSTALLATION_MODE    = 0x02
    STATUS_OFFSET_ACQUISITION_MODE      = 0x03
    STATUS_SELFTEST_MODE                = 0x04

    def __init__(self, dodiag=False):
        self.I2C_ADDR = 0x55
        i2c.try_lock()
        print(i2c.scan())
        i2c.unlock()
        self.device = I2CDevice(i2c, self.I2C_ADDR)
        print(dir(self.device))

        self.writeByte(self.REG_CTRL, 0x04)
        time.sleep(2.0)
        if dodiag:
            self.writeByte(self.REG_MODE, 0x04)
        else:
            self.writeByte(self.REG_MODE, 0x02)

        time.sleep(2.0)

    def setState(self
    def getState(self):
        status = self.readByte(self.REG_STATE)
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
            si /= 10
        return si

    def getInstantaneusPGA(self):
        pga = self.readByte16(self.REG_PGA_H)
        return pga

    #
    # I2C IO Functions
    #
    def readByte(self,register16):

        try:
            with self.device:
                buf = register16.to_bytes(2, 'big')
                self.device.write(buf)
                data = bytearray(1)
                self.device.readinto(data)
            return data
        except OSError:
            return None

    def readByte16(self,register16):
        datah = self.readByte(register16)
        datal = self.readByte(register16+1)

        print('r16', datah, datal)
        if datah is not None and datal is not None:
            return (datah[0] << 8) | (datal[0] & 0xFF)
        return None

    def writeByte(self,register16, data):

        buf = register16.to_bytes(2, 'big')
        buf += data.to_bytes(1,'big')
        print('BUF', buf)
        print('buf type', type(buf))

        with self.device:
            self.device.write(buf)

    def writeByte16(self,register16, data16):
        buf = register16.to_bytes(2, 'big')
        buf += data.to_bytes(2,'big')
        with self.device:
            self.device.write(buf)

