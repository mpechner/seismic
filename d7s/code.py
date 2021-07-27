# Write your code here :-)
# coding: utf-8
# Sample that outputs the value acquired by D7S.

#from __future__ import print_function

import time
#import datetime

import grove_d7s


# sensor.enter_diag()
def get_diags():
    sensor = grove_d7s.GroveD7s()
    if sensor.isReady() == False:
        print('.')
        time.sleep(1.0)

    print ("start diag")


def waiton():
    sensor = grove_d7s.GroveD7s()
    while sensor.isReady() == False:
        print('.')
        time.sleep(1.0)



    print ("start")
    print(sensor.getInstantaneusSI())
    while True:
          time.sleep(1.0)
          if sensor.isEarthquakeOccuring() == True:
              si = sensor.getInstantaneusSI()
              pga = sensor.getInstantaneusPGA()
              now = datetime.datetime.today()

              if si == None or pga == None:
                  continue

              #print(now.strftime("[%Y/%m/%d %H:%M:%S]")
              #          ,"SI=%.1f[Kine]" %si,"PGA=%d[gal]" %pga)

if __name__ == '__main__':
  get_diags()
