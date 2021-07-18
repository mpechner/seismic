import board
#import neopixel
import time
import busio
import math
import json
from adafruit_magtag.magtag import MagTag
from secrets import secrets
from time import sleep
from gc import collect
import alarm
from alarm.pin import PinAlarm
from adafruit_portalbase import PortalBase


#resp = json.loads('{"type":"Point","coordinates":[-178.3804,-20.6238,559.13]}')
#print(resp)



eq_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
# eq_url = "http://wedding.mikey.com/fmt.json"

# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
# Thanks Fred W6BSD for python from stack overflow
#

def distance(origin, dest):
    lat1, lon1 = origin
    lat2, lon2 = dest
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def azimuth(origin, dest):
    lat1, lon1 = origin
    lat2, lon2 = dest

    dLon = (lon2 - lon1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = math.atan2(x, y)
    brng = math.degrees(brng)
    return int(brng)

#############################
def deep_sleep():
    last_line = "Refresh"
    magtag.add_text(  # text_font="/fonts/Lato-Bold-ltd-25.bdf",
        text_position=(1, 121),
        is_data=False,
        text=last_line

    )
    alarms.append(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 14400))
    alarm.exit_and_deep_sleep_until_alarms(*alarms)

def clear_display():
    magtag.graphics.set_background(0xFFFFFF)

def flashit(fillset):
    for ii in range(0, 4):
        magtag.peripherals.play_tone(440, 0.15)
        magtag.peripherals.neopixels.fill(fillset)
        time.sleep(.25)
        magtag.peripherals.neopixels.fill((0, 0, 0))
        time.sleep(.25)

def get_data():
    # pbase = PortalBase()

    for dotry in range(1):
        try:
            magtag.url = eq_url
            fetched_data = magtag.fetch()
            #magtag.network.connect()
            #fetched_data = magtag.network.fetch(eq_url,headers={"Content-type":"application/json; charset=utf-8 "})

            # print("FETCHED", fetched_data)
            # time.sleep(60)

            eq_data = json.loads(fetched_data)
            # print("\n \nEQ DATA", eq_data)
            return eq_data
        except Exception as ex:
            print(ex)
            time.sleep(3)
    return None

buttons = [board.BUTTON_A]
alarms = [alarm.pin.PinAlarm(pin=pin, value=False, pull=True) for pin in buttons]

magtag = MagTag()

if magtag.peripherals.battery < 2.9:
    for ii in range(0, 10) :
        magtag.peripherals.play_tone(3000, 1.0)
        sleep(1)
    magtag.add_text(
        text_position=(40, 60),
        is_data=False,
        text_scale=3,
        text="BATTERY LOW"
    )
    magtag.exit_and_deep_sleep(7200)

local_lat = 37.35253
local_long = -121.99609

eq_data = get_data()
if not eq_data:
    deep_sleep()

event_list = {}
for event in eq_data['features']:
    # print(event['geometry'])
    # print(type(event['geometry']['coordinates'][0]))
    dist = distance([local_lat, local_long], [event['geometry']['coordinates'][1], event['geometry']['coordinates'][0]])
    # print ( dist, event['properties']['place'], event['properties']['mag'], [event['geometry']['coordinates'][0], event['geometry']['coordinates'][1]])
    event_list[int(dist)] = "%5.1fkm %1.1f %s" % (dist, event['properties']['mag'],event['properties']['place'] )

magtag.add_text(
    text_position=(5,11),
    is_data=False,
    text_scale = 2)
magtag.set_text("EQ 2.5+ Last 24H", index=0, auto_refresh=False)

list_ev = sorted(event_list.keys())
for ev in  list_ev:
    print(ev, event_list[ev])

line = 1
for ev in  list_ev:
    # print(event_list[ev])
    magtag.add_text(
    text_position=(5, 20 +(line * 11)),
    is_data=False)
    magtag.set_text(event_list[ev], index=line, auto_refresh=False)

    line += 1

    if ev < 200:
        flashit((0,128,0))
    if line > 7:
        break

deep_sleep()
