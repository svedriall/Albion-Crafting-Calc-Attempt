from django.db import models
from django.utils import timezone


class Food(models.Model):
    food_name = models.CharField(max_length=50)
    food_ID = models.CharField(max_length=50)
    food_price = models.CharField(max_length=50)


    def publish(self):
        self.published_date = timezone.now()

    def food_definition(self):
        return '{}'.format(self.food_name, self.food_ID, self.food_price)

    def __str__(self):
        return self.food_definition