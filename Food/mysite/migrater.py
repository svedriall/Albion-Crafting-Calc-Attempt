import xml.etree.ElementTree as ET
import json
import urllib
from urllib.request import Request, urlopen

parser = ET.XMLParser(encoding="utf-8")

tree = ET.parse('items.xml')
root = tree.getroot()


def Pricer(item_id):
    page = "https://www.albion-online-data.com/api/v2/stats/prices/" + item_id + "?locations=Caerleon&qualities=0"
    file = urllib.request.urlopen(page)
    data = file.read()
    mydata = json.loads(data)
    price = 0
    for t in range(len(mydata)):
        price = int(mydata[0]['sell_price_min'])
    return price;


def Req_Pricer(item_id, level):
    page = "https://www.albion-online-data.com/api/v2/stats/prices/" + item_id + "?locations=Caerleon&qualities=0"
    file = urllib.request.urlopen(page)
    data = file.read()
    mydata = json.loads(data)
    resc_price = 0
    resc_total = 0
    for t in range(len(mydata)):
        resc_price = int(mydata[0]['sell_price_min'])
        resc_count = int(level.get('count'))
        resc_total = resc_count * resc_price
    return resc_price, resc _total;


# list = ['consumableitem', 'farmableitem', 'simpleitem', 'consumablefrominventoryitem', 'equipmentitem', 'weapon', 'mount', 'furnitureitem', 'journalitem']
list = ['consumableitem']

# for tags in root:
#     if tags.tag not in list:
#         list.append(tags.tag)
for iterate in list:
    for consumableitem in root.findall(iterate):
        uniqueid = consumableitem.get('uniquename')
        tier = consumableitem.get('tier')
        weight = consumableitem.get('weight')
        shopcategory = consumableitem.get('shopcategory')
        shopsubcategory = consumableitem.get('shopsubcategory1')
        slottype = consumableitem.get('slottype')
        nutrition = consumableitem.get('nutrition')

        price = Pricer(uniqueid)
        print("- ID:", uniqueid,
              "- Tier:", tier,
              "- Weight:", weight,
              "- Slot:", slottype,
              "- Cat:", shopcategory,
              "- Subcat:", shopsubcategory,
              "- Price: ", price,
              "- Nutrition: ", nutrition,)

        # CRAFTING REQUIREMENTS #
        for craftingrequirements in consumableitem.findall('craftingrequirements'):

            amountcrafted = craftingrequirements.get('amountcrafted')
            craftingfocus = craftingrequirements.get('craftingfocus')

            print("- FCS:", craftingfocus, 'Crft Amt:', amountcrafted)
            for reqCrafts in craftingrequirements.findall('craftresource'):
                req_name = reqCrafts.get('uniquename')
                req_count = int(reqCrafts.get('count'))
                maxreturnamount = reqCrafts.get('maxreturnamount')

                total = Req_Pricer(req_name, reqCrafts)

                print("->", "ID:", req_name, "Count:", req_count, "Total Price:", total, "MaxReturn: ", maxreturnamount)
        # ENCHANTED ITEM DETAILS #
        for enchantments in consumableitem.findall('enchantments'):
            for enchantment in enchantments.findall('enchantment'):
                print("ID:", uniqueid, "Enchant:", enchantment.get('enchantmentlevel'))
                # CRAFT SOURCES #
                for craftreq in enchantment.findall('craftingrequirements'):
                    for craftresource in craftreq.findall('craftresource'):
                        resc_name = craftresource.get('uniquename')
                        resc_count2 = craftresource.get('count')

                        total2 = Req_Pricer(resc_name, craftresource)

                        print("->", "Resc ID:", resc_name, "- Count:", resc_count2, '- Total:', total2)
        print("\n")
print(list)
