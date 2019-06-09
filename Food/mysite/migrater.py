import xml.etree.ElementTree as ET
import json
import urllib
from urllib.request import Request, urlopen

parser = ET.XMLParser(encoding="utf-8")

tree = ET.parse('items.xml')
root = tree.getroot()



# for consumableitem in root.findall('consumableitem'):
#     name = consumableitem.get('uniquename')
#     print(name)
#     abilitypower = consumableitem.get('abilitypower')
#     amountcrafted = consumableitem.get('amountcrafted')
#     for craftingrequirements in consumableitem:
#         for enchantments in consumableitem.findall('enchantments'):
#             for enchantment in enchantments.findall('enchantment'):
#                 print("Level: ",enchantment.get('enchantmentlevel'))
#                 for x in enchantment.findall('craftresource'):
#                     print(craftsource.get('uniquename'))
#         for craftsource in craftingrequirements.findall('craftresource'):
#             print("-->",craftsource.get('uniquename'),craftsource.get('count'))

# for consumableitem in tree.iter('consumableitem'):
#     print(consumableitem.attrib)
#     print(" ")
#     for craftingrequirements in consumableitem:
#         print(craftingrequirements.attrib)
#         for craftresource in craftingrequirements:
#             print(craftresource.get('uniquename'),craftresource.get('count'))


# for items in tree.iter('weapon'):
#     if items not in output:
#         output.append(items.get('uniquename'))
# for x in output:
#     print(x)

# for items in tree.iter():
#     print(items.get('uniquename'))

# list = ['farmableitem', 'simpleitem', 'consumableitem', 'consumablefrominventoryitem', 'equipmentitem', 'weapon', 'mount', 'furnitureitem', 'journalitem']
list = ['consumableitem']

# for tags in root:
#     if tags.tag not in list:
#         list.append(tags.tag)
for iterate in list:
    for consumableitem in root.findall(iterate):
        uniqueid = consumableitem.get('uniquename')
        amountcrafted = consumableitem.get('amountcrafted')
        tier = consumableitem.get('tier')
        weight = consumableitem.get('weight')
        shopcategory = consumableitem.get('shopcategory')
        shopsubcategory = consumableitem.get('shopsubcategory1')
        craftingfocus = consumableitem.get('craftingfocus')
        slottype = consumableitem.get('slottype')

        page = "https://www.albion-online-data.com/api/v2/stats/prices/" + uniqueid + "?locations=Caerleon&qualities=0"
        file = urllib.request.urlopen(page)
        data = file.read()
        mydata = json.loads(data)

        for t in range(len(mydata)):
            price = mydata[0]['sell_price_min']

        print("- ID:",uniqueid,
              "- Tier:",tier,
              "- Amount:", amountcrafted,
              "- Weight:", weight)
        print("- Slot:", slottype,
              "- FCS:",craftingfocus,
              "- Cat:", shopcategory,
              "- Subcat:", shopsubcategory,
              "Price: ", price)

        # CRAFTING REQUIREMENTS #
        for craftingrequirements in consumableitem.findall('craftingrequirements'):
            for reqCrafts in craftingrequirements.findall('craftresource'):

                page2 = "https://www.albion-online-data.com/api/v2/stats/prices/" + reqCrafts.get('uniquename') + "?locations=Caerleon&qualities=0"
                file2 = urllib.request.urlopen(page2)
                data2 = file2.read()
                mydata2 = json.loads(data2)

                for t in range(len(mydata)):
                    req_price = int(mydata2[0]['sell_price_min'])
                    total = int(reqCrafts.get('count')) * req_price

                print("->", "ID:", reqCrafts.get('uniquename'),"Count:", reqCrafts.get('count'), "ReqPrice:",total)
        # ENCHANTED ITEM DETAILS #
        for enchantments in consumableitem.findall('enchantments'):
            for enchantment in enchantments.findall('enchantment'):
                print("ID:", uniqueid, "Enchant:", enchantment.get('enchantmentlevel'))
                # CRAFT SOURCES #
                for craftreq in enchantment.findall('craftingrequirements'):
                    for craftresource in craftreq.findall('craftresource'):
                        print("->", "ID:", craftresource.get('uniquename'), "Count:",craftresource.get('count'))
        print("\n")
print(list)
