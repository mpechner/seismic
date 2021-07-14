# seismic

## ToDo
* Connect Seismic Sensor, set alarm, display event
* Connect GPS or SD. SD, put secrets.py and local lat long on card.

Well I screwed up.  The earthquake click has their own libraries.  I will dig into code from omron to figure out how to interface with circuit python. The board just seems to expose I2C.  But there are 2 other pins, int, int2 and setup I need to figureout. At $69, I'm not tossing the board.

* Python https://github.com/omron-devhub/d7s-grove-raspberrypi/blob/master/README.md#d7s-grove-raspberrypi
* arduino C++ https://github.com/omron-devhub/d7s-grove-arduino

## Secrets.py
Do not check in secrets.py.  Just place at the top level of the project with code.py.
```python
secrets = {
   "ssid":"SSID",
    "password":"passwd"
}
```
# Hardware
Controller AdaFruit MagTag https://www.adafruit.com/product/4800

Seismic Sensor https://www.mikroe.com/earthquake-click

GPS: https://www.adafruit.com/product/4415

Power: https://www.adafruit.com/product/328


## Math
### Distance between 2 lat/long
https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula

### convert from lat/long degress minutes to decimal
https://www.latlong.net/degrees-minutes-seconds-to-decimal-degrees

## Data Feed
* https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
* 4.5+ last 24 hours https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson
* 2.5+ last 24 hours https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson

## Requirements
* adafruit_bitmap_font
* adafruit_display_text
* adafruit_io
* adafruit_magtag
* adafruit_portalbase
* adafruit_requests.mpy
* neopixel.mpy
* simpleio.mpy
