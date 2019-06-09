import json
import urllib
from urllib.request import Request, urlopen

uniqueid = "T8_MEAL_STEW"
page = "https://www.albion-online-data.com/api/v2/stats/prices/" + uniqueid + "?locations=Caerleon&qualities=0"
file = urllib.request.urlopen(page)
data = file.read()
mydata = json.loads(data)

print(json.dumps(mydata))

# for t in range(len(mydata)):
#    print(mydata[0]['buy_price_max'])