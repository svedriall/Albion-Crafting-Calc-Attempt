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

## SLOT TYPES:
# food, potion, None, offhand, cape, bag, head, armor, shoes, mainhand, mount

## SHOP CATEGORIES:
# consumables, farmables, products, materials, luxurygoods, other, token, resources,
# artefacts, cityresources, offhand, accessories, armor, melee, gatherergear, tools,
# ranged, magic, mounts, furniture, trophies

## SHOP SUB CATEGORIES:
# fish, potion, fishingbait, cooked, vanity, seed, animals, farming, other, martlock,
# lymhurst, fortsterling, thetford, bridgewatch, caerleon, mission, arenasigils, maps,
# royalsigils, event, wood, rock, ore, hide, fiber, planks, stoneblock, metalbar, leather,
# cloth, magic_artefact, ranged_artefact, melee_artefact, offhand_artefact, armor_artefact,
# essence, rune, soul, relic, trash, treeheart, rockheart, beastheart, mountainheart, vineheart,
# skillbook, shield, book, orb, totem, torch, horn, cape, bag, unique_helmet, unique_armor,
# unique_shoes, mace, leather_helmet, leather_armor, leather_shoes, plate_helmet, plate_armor,
# plate_shoes, cloth_helmet, cloth_armor, cloth_shoes, fibergatherer_helmet, fibergatherer_armor,
# fibergatherer_shoes, fibergatherer_backpack, hidegatherer_helmet, hidegatherer_armor, hidegatherer_shoes,
# hidegatherer_backpack, oregatherer_helmet, oregatherer_armor, oregatherer_shoes, oregatherer_backpack,
# rockgatherer_helmet, rockgatherer_armor, rockgatherer_shoes, rockgatherer_backpack, woodgatherer_helmet,
# woodgatherer_armor, woodgatherer_shoes, woodgatherer_backpack, fishgatherer_helmet, fishgatherer_armor,
# fishgatherer_shoes, fishgatherer_backpack, pickaxe, stonehammer, woodaxe, sickle, skinningknife,
# demolitionhammer, fishing, crossbow, bow, cursestaff, firestaff, froststaff, arcanestaff, holystaff,
# naturestaff, dagger, spear, axe, sword, quarterstaff, hammer, rare_mount, ridinghorse, armoredhorse,
# ox, repairkit, flag, banner, chest, unique, bed, table, decoration_furniture, morgana_furniture, keeper
# _furniture, heretic_furniture, generaltrophy, mercenarytrophy, hidetrophy, oretrophy, fibertrophy,
# rocktrophy, woodtrophy, fishtrophy, journal

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
        elif item_main_id.find('_LEVEL3') != -1:
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
        item_main_id = str(item.get('uniquename'))
        temp_id = str(item.get('uniquename'))
        item_main_tier = item.get('tier')
        item_main_weight = item.get('weight')
        item_main_shopcategory = item.get('shopcategory')
        item_main_shopsubcategory = item.get('shopsubcategory1')
        item_main_slottype = item.get('slottype')
        #### WHAT TO SUBCAT ####
        if item_main_shopsubcategory != "fish":
            # price = Pricer(uniqueid)
            temp_count_list = []

            item_main_nutrition = item.get('nutrition')
            if item_main_nutrition is None:
                item_main_nutrition = "Not Food"

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

            for craftingrequirements in item.findall('craftingrequirements'):

                item_main_amountcrafted = craftingrequirements.get('amountcrafted')
                if item_main_amountcrafted is None:
                    item_main_amountcrafted = "1"

                item_main_craftingsource = craftingrequirements.get('craftingfocus')
                if item_main_craftingsource is None:
                    item_main_craftingsource = "Not Craftable"

                # print("| Crft. Focus:", craftingfocus, '- Crafted Amount:', amountcrafted)
                item_main_resource_count_list = []
                item_main_resource_list = []
                for CraftingRequirements_Attrib in craftingrequirements.findall('craftresource'):
                    item_main_resource_id = CraftingRequirements_Attrib.get('uniquename')
                    item_main_resource_count = str(CraftingRequirements_Attrib.get('count'))

                    item_main_resource_maxreturnamount = CraftingRequirements_Attrib.get('maxreturnamount')
                    if item_main_resource_maxreturnamount is None:
                        item_main_resource_maxreturnamount = "0"
                    # req_main_name = Namer(req_main_id)

                    item_main_resource_list.append(item_main_resource_id)
                    item_main_resource_count_list.append(item_main_resource_count)

                    # total = Req_Pricer(req_main_id, CraftingRequirements_Attrib)
                    # print("->", "ID:", req_main_name, "Count:", req_main_count, "Total Price:", total, "MaxReturn: ",maxreturnamount)

            # ENCHANTED ITEM DETAILS #


            temp_list = []
            temp_count_list = []
            temp_list = str(",".join(item_main_resource_list))
            temp_count_list = ",".join(item_main_resource_count_list)
            print(item_main_id, ":", temp_list, temp_count_list)
            c.execute("INSERT INTO Components VALUES ('" + item_main_id + "','" + temp_list + "','" + temp_count_list + "')");
            # x = "INSERT INTO Components VALUES ('" + uniqueid + ",'" + newlist + "')"




            # print(x)
            # c.execute(x);
            for enchantments in item.findall('enchantments'):
                for enchantment in enchantments.findall('enchantment'):
                    enchantmentlevel = enchantment.get('enchantmentlevel')
                    item_ench_resource_list = []  # CLEAR ENCHANTED ITEM RESOURCES LIST
                    item_ench_resource_count_list = []

                    item_main_id = temp_id + "@" + enchantmentlevel  # GET TEMP ID FOR ENCHANTED ITEM

                    # print("ID:", uniqueid, "Enchant:", enchantment.get('enchantmentlevel'))
                    # CRAFT SOURCES #
                    for item_ench_req in enchantment.findall('craftingrequirements'):
                        temp_list = [] # CREATE NEW DB LIST
                        for item_ench in item_ench_req.findall('craftresource'):

                            item_ench_resource_id = item_ench.get('uniquename')  # ENCHANTED SOURCE LOOP
                            item_ench_resource_count = item_ench.get('count') #  ENCHANTED SOURCE COUNT LOOP
                            item_ench_resource_list.append(item_ench_resource_id)  # ADDING SOURCES TO LIST
                            item_ench_resource_count_list.append(item_ench_resource_count)

                            # resc_name = Namer(resc_id)
                            # total2 = Req_Pricer(resc_id, item_ench)
                            # print("->", "Resc ID:", resc_id, "- Count:", resc_count2, '- Total:')
                        ### DB INSERTION ENCHANTED ###

                        temp_list = str(",".join(item_ench_resource_list))
                        temp_count_list = str(",".join(item_ench_resource_count_list))
                        print(item_main_id, ":", temp_list,temp_count_list)
                        c.execute("INSERT INTO Components VALUES ('" + item_main_id + "','" + temp_list + "','" + temp_count_list + "')");

                        ###############################
            # print("\n")
# print(list)
print("######### SUCCESS #########")

conn.commit();
conn.close();
