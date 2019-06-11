from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient
import json
import urllib
from urllib.request import Request, urlopen
import os


# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in '%s': %s" % (cwd, files))

def data_list(request):
    ingredients_view = Ingredient.objects.all().order_by('ingredient_ID')
    # requirement_list("T6_MEAL_STEW")



    return render(request, 'AlbionCraft/data_list.html', {'Ingredient': ingredients_view})
    # return render(request, 'AlbionCraft/data_list.html')


def requirement_list(ITEM_ID):
    page = "https://gameinfo.albiononline.com/api/gameinfo/items/" + ITEM_ID + "/data/"
    file = urllib.request.urlopen(page)
    data = file.read()
    mydata = json.loads(data)
    Enchantments = mydata['enchantments']['enchantments']

    for t in range(len(Enchantments)):
        Crafting_Requirements = Enchantments[t]['craftingRequirements']['craftResourceList']
        if t == 0:
            Crafting_lenght = len(Crafting_Requirements) - 1
            print(mydata['uniqueName'])
            print(mydata['itemType'])
            for i in range(Crafting_lenght):
                print(Crafting_Requirements[i])

        Crafting_lenght = len(Crafting_Requirements)
        print("--- Tier ", t + 1, "---")
        print(mydata['uniqueName'])
        print(mydata['itemType'])
        for i in range(Crafting_lenght):
            print(Crafting_Requirements[i])
