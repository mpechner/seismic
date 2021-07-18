import requests
import json
import math


# eq_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
eq_url = "http://wedding.mikey.com/fmt_c.json"


def distance(origin, dest):
    lat1, lon1 = origin
    lat2, lon2 = dest
    print(lat1, lon1, lat2, lon2)
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c

local_lat = 37.35253
local_long = -121.99609


resp = requests.get(eq_url)
eq_data  = json.loads(resp.content)
print(json.dumps(eq_data, indent=4))

event_list = {}
for event in eq_data['features']:
    print([event['geometry']['coordinates'][0], event['geometry']['coordinates'][1]])
    dist = distance([local_lat, local_long], [event['geometry']['coordinates'][1], event['geometry']['coordinates'][0]])
    print ( dist, event['properties']['place'], event['properties']['mag'])
    event_list[dist] = "%5.0fkm %1.1f %s" % (dist, event['properties']['mag'],event['properties']['place'] )

list_ev = sorted(event_list.keys())
line = 1
for ev in  list_ev:
    print(event_list[ev])
    print(event_list[ev])

    line += 1

