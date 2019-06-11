import xml.etree.ElementTree as ET
import json
import urllib
from urllib.request import Request, urlopen
from urllib.error import HTTPError


parser = ET.XMLParser(encoding="utf-8")

tree = ET.parse('items.xml')
root = tree.getroot()


failed_prices_list = []
failed_names_list = []
shopcategory_list = []
shopsubcategory_list = []
slottype_list = []
def Pricer(item_id):
    try:
        page = "https://www.albion-online-data.com/api/v2/stats/prices/" + item_id + "?locations=Caerleon&qualities=0"
        file = urllib.request.urlopen(page)
        data = file.read()
        mydata = json.loads(data)
        if mydata[0]['sell_price_min'] is not None:
            for t in range(len(mydata)):
                price = int(mydata[0]['sell_price_min'])
                print("success")
        else:
            failed_prices_list.append(item_id)
            price = "Failed - Saved"
            print(item_id, " !!!!! failed to get price !!!!!")
    except HTTPError:
        price = 101010
        print(item_id, "500 Error")
    except IndexError:
        price = 101010
        print(item_id," Item not found")
    return price;


def Req_Pricer(item_id, level):
    try:
        page = "https://www.albion-online-data.com/api/v2/stats/prices/" + item_id + "?locations=Caerleon&qualities=0"
        file = urllib.request.urlopen(page)
        data = file.read()
        mydata = json.loads(data)
        resc_price = 0
        resc_total = 0
        for t in range(len(mydata)):
            try:
                resc_price = int(mydata[0]['sell_price_min'])
                resc_count = int(level.get('count'))
                resc_total = resc_count * resc_price
            except:
                resc_price = 101010
                failed_prices_list.append(item_id)
                print(item_id + "failed to catch price")
    except HTTPError:
        resc_price = 101010
        resc_total = 101010

    return resc_price, resc_total;


def Namer(item_id):
    try:
        if item_id.find('_LEVEL1') != -1:
            item_id = item_id.replace('_LEVEL1@', '@')
        elif item_id.find('_LEVEL2') != -1:
            item_id = item_id.replace('_LEVEL2@', '@')
        elif uniqueid.find('_LEVEL3') != -1:
            item_id = item_id.replace('_LEVEL3@', '@')
        page = "https://gameinfo.albiononline.com/api/gameinfo/items/" + item_id + "/data"
        file = urllib.request.urlopen(page)
        data = file.read()
        mydata = json.loads(data)
        try:
            resc_itemname = json.dumps(mydata['localizedNames']['EN-US'])
        except TypeError:
            resc_itemname = "Name not Localized"
            failed_names_list.append(item_id)
            print(item_id + "failed to catch name")
    except HTTPError:
        resc_itemname = "500 ERROR - WRONG ID"
    return resc_itemname;


uniqueid = "T3_VANITY_CONSUMABLE_FIREWORKS_BLUE"
# uniqueid = "T6_RANDOM_DUNGEON_TOKEN_3"
x = Pricer(uniqueid)

list = ['consumableitem', 'farmableitem', 'simpleitem', 'consumablefrominventoryitem', 'equipmentitem', 'weapon', 'mount', 'furnitureitem', 'journalitem']


# for iterate in list:
#     for consumableitem in root.findall(iterate):
#         shopcategory = consumableitem.get('shopcategory')
#         shopsubcategory = consumableitem.get('shopsubcategory1')
#         slottype = consumableitem.get('slottype')
#         uniqueid = consumableitem.get('uniquename')


        # print(slottype,shopcategory,shopsubcategory)
        #
        # if shopcategory not in shopcategory_list:
        #     shopcategory_list.append(shopcategory)
        # if shopsubcategory not in shopsubcategory_list:
        #     shopsubcategory_list.append(shopsubcategory)
        # if slottype not in slottype_list:
        #     slottype_list.append(slottype)

# print(*slottype_list, sep = ", ")
# print("\n")
# print(*shopcategory_list, sep = ", ")
# print("\n")
# print(*shopsubcategory_list, sep = ", ")

# print(*failed_names_list, sep = ", ")
# print(*failed_prices_list, sep = ", ")




# for t in range(len(mydata)):
#    print(mydata[0]['buy_price_max'])