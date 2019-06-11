import xml.etree.ElementTree as ET
from django.db import models


class XMLIMPORT(models.model):
    root = ET.parse('bin/items.xml').getroot()

    def __str__(self):
        return self.ingredient_definition()
        return self.ingredient_name()