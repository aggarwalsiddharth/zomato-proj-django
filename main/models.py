from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models import Avg
# Create your models here.

class Restaurant(models.Model):
    City_ID = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    average_cost_for_two = models.IntegerField()
    menu_link = models.URLField()
    photo_link = models.URLField()
    thumbnail = models.CharField(max_length=1000)

    def get_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500, null=True,blank=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    display_pic = models.CharField(max_length=1000)

    def __str__(self):
        return self.title