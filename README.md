# seismic
![Seismic](https://github.com/mpechner/seismic/blob/main/images/image.jpg)
## ToDo
* Connect Seismic Sensor, set alarm, display event
* Connect GPS or SD. SD, put secrets.py and local lat long on card.

### Seismic Sensor
Well I screwed up.  The earthquake click has their own libraries.  I will dig into code from omron to figure out how to interface with circuit python. The board just seems to expose I2C.  But there are 2 other pins, int, int2 and setup I need to figureout. At $69, I'm not tossing the board.

Did not screw up.   The board is a basic reference design. 

#### Circuit Python Code
There is a bunch of code from omron.
* The chips data sheet https://download.mikroe.com/documents/datasheets/d7s-datasheet.pdf - not alot here.
* Python https://github.com/omron-devhub/d7s-grove-raspberrypi/blob/master/README.md#d7s-grove-raspberrypi
** grove_d7s.py needs to be ported to use Adafruit I2C libraries instead of smbus2 as well as the Pi GPIO definitions.

Here are the various circuit python I2C Libraries to examine.  see which replaces smbus, or wraps it.
* https://github.com/adafruit/Adafruit_CircuitPython_Debug_I2C
* https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* https://github.com/adafruit/Adafruit_CircuitPython_Register
* https://github.com/adafruit/Adafruit_Python_PureIO
* https://github.com/adafruit/Adafruit_CircuitPython_BitbangIO

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
