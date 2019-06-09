from django.db import models
from django.utils import timezone


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50)
    ingredient_ID = models.CharField(max_length=50)
    ingredient_price = models.IntegerField()


    def publish(self):
        self.published_date = timezone.now()

    def ingredient_definition(self):
        return '{}'.format(self.ingredient_name, self.ingredient_ID, self.ingredient_price)

    def __str__(self):
        return self.ingredient_definition()
        return self.ingredient_name()