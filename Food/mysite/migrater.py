import xml.etree.ElementTree as ET
import json
import urllib
from urllib.request import Request
from urllib.error import HTTPError
import sqlite3
conn = sqlite3.connect('AO.db')

c = conn.cursor();

# ITERATE HERE


# END ITERATE


parser = ET.XMLParser(encoding="utf-8")

tree = ET.parse('items.xml')
root = tree.getroot()

failed_prices_list = []
failed_names_500_list = []
failed_names_localized_list = []

def Pricer(item_id):
    global price
    try:
        page = "https://www.albion-online-data.com/api/v2/stats/prices/" + item_id + "?locations=Caerleon&qualities=0"
        file = urllib.request.urlopen(page)
        data = file.read()
        mydata = json.loads(data)
        if mydata[0]['sell_price_min'] is not None:
            for t in range(len(mydata)):
                price = int(mydata[0]['sell_price_min'])
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
        if mydata[0]['sell_price_min']:
            for t in range(len(mydata)):
                try:
                    resc_price = int(mydata[0]['sell_price_min'])
                    resc_count = int(level.get('count'))
                    resc_total = resc_count * resc_price
                except:
                    resc_price = 101010
                    failed_prices_list.append(item_id)
                    print(item_id + "failed to catch price")
        else:
            failed_prices_list.append(item_id)
            resc_price = "Failed - Saved"
            print(item_id, " !!!!! failed to get price !!!!!")
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
            failed_names_localized_list.append(item_id)
            print(item_id + "failed to catch name")
    except HTTPError:
        resc_itemname = "500 ERROR - WRONG ID"
        failed_names_500_list.append(item_id)
    return resc_itemname;

list = ['consumableitem', 'farmableitem', 'simpleitem', 'consumablefrominventoryitem', 'equipmentitem', 'weapon', 'mount', 'furnitureitem', 'journalitem']
# list = ['consumableitem']

# for tags in root:
#     if tags.tag not in list:
#         list.append(tags.tag)

for iterate in list:
    for item in root.findall(iterate):
        #### MAIN ITEM INFO #####
        uniqueid = str(item.get('uniquename'))
        temp_id = str(item.get('uniquename'))
        tier = item.get('tier')
        weight = item.get('weight')
        shopcategory = item.get('shopcategory')
        shopsubcategory = item.get('shopsubcategory1')
        slottype = item.get('slottype')
        #### WHAT TO SUBCAT ####
        if shopsubcategory == "cooked":
            # price = Pricer(uniqueid)

            nutrition = item.get('nutrition')
            if nutrition is None:
                nutrition = "Not Food"

            # item_name = Namer(uniqueid)
            # if item_name == "500 ERROR - WRONG ID":
            #     item_name = uniqueid

            # print("####   " + item_name + "   ####")
            # print("| ID:", uniqueid,
            #       "| Price: ", price,
            #       "| Tier:", tier)
            #
            # print("| Slot:", slottype,
            #       "| Cat:", shopcategory,
            #       "| Subcat:", shopsubcategory)
            #
            # print("| Nutrition: ", nutrition,
            #       "| Weight:", weight, )

            # CRAFTING REQUIREMENTS #
            for craftingrequirements in item.findall('craftingrequirements'):

                amountcrafted = craftingrequirements.get('amountcrafted')
                if amountcrafted is None:
                    amountcrafted = "1"

                craftingfocus = craftingrequirements.get('craftingfocus')
                if craftingfocus is None:
                    craftingfocus = "Not Craftable"

                # print("| Crft. Focus:", craftingfocus, '- Crafted Amount:', amountcrafted)
                req_main_list = []
                for CraftingRequirements_Attrib in craftingrequirements.findall('craftresource'):
                    req_main_id = CraftingRequirements_Attrib.get('uniquename')
                    req_main_count = int(CraftingRequirements_Attrib.get('count'))

                    maxreturnamount = CraftingRequirements_Attrib.get('maxreturnamount')
                    if maxreturnamount is None:
                        maxreturnamount = "0"
                    # req_main_name = Namer(req_main_id)
                    req_main_list.append(req_main_id)

                    # total = Req_Pricer(req_main_id, CraftingRequirements_Attrib)
                    # print("->", "ID:", req_main_name, "Count:", req_main_count, "Total Price:", total, "MaxReturn: ",maxreturnamount)
            # ENCHANTED ITEM DETAILS #
            newlist = []
            newlist = str(",".join(req_main_list))
            print(uniqueid,":",newlist)
            c.execute("INSERT INTO Components VALUES ('" + uniqueid + "','" + newlist + "')");
            # x = "INSERT INTO Components VALUES ('" + uniqueid + ",'" + newlist + "')"
            # print(x)
            # c.execute(x);
            for enchantments in item.findall('enchantments'):
                for enchantment in enchantments.findall('enchantment'):
                    enchantmentlevel = enchantment.get('enchantmentlevel')
                    uniqueid = temp_id + "@" + enchantmentlevel
                    # print("ID:", uniqueid, "Enchant:", enchantment.get('enchantmentlevel'))
                    # CRAFT SOURCES #
                    for craftreq in enchantment.findall('craftingrequirements'):
                        req_main_list = []
                        newlist = []
                        for craftresource in craftreq.findall('craftresource'):

                            resc_id = craftresource.get('uniquename')
                            resc_count2 = craftresource.get('count')
                            req_main_list.append(resc_id)

                            # resc_name = Namer(resc_id)
                            # total2 = Req_Pricer(resc_id, craftresource)

                            # print("->", "Resc ID:", resc_id, "- Count:", resc_count2, '- Total:')

                        newlist = str(",".join(req_main_list))
                        print(uniqueid, ":", newlist)
                        c.execute("INSERT INTO Components VALUES ('" + uniqueid + "','" + newlist + "')");
            # print("\n")
# print(list)
print("######### SUCCESS #########")
print(*failed_names_localized_list, sep=", ")
# print("\n")
print(*failed_prices_list, sep=", ")

conn.commit();
conn.close();
