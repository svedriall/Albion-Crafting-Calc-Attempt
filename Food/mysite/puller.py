import json
import urllib
from urllib.request import Request, urlopen
resc_itemdescription = ""
def req_namer(uniqueid):
    if uniqueid.find('_LEVEL1') != -1:
        uniqueid = uniqueid.replace('_LEVEL1', '')
    elif uniqueid.find('_LEVEL2') != -1:
        uniqueid = uniqueid.replace('_LEVEL2', '')
    elif uniqueid.find('_LEVEL3') != -1:
        uniqueid = uniqueid.replace('_LEVEL3', '')
    page = "https://gameinfo.albiononline.com/api/gameinfo/items/"+uniqueid+"/data"
    file = urllib.request.urlopen(page)
    data = file.read()
    mydata = json.loads(data)

    resc_itemname = json.dumps(mydata['localizedNames']['EN-US'])
    resc_itemdescription = json.dumps(mydata['localizedDescriptions']['EN-US'])
    return resc_itemname, resc_itemdescription;

uniqueid = "T1_FISH_FRESHWATER_ALL_COMMON"
# uniqueid = "T8_MEAL_STEW"
x, y = req_namer(uniqueid)
print(x, y)



# for t in range(len(mydata)):
#    print(mydata[0]['buy_price_max'])