from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Flower(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  color = models.CharField(max_length=100)
  img = models.CharField(max_length=200)
  price_stem = models.IntegerField()
 
  def __str__(self):
    # This must return a string
    return f"The flower named '{self.name}' is {self.color} in color. It is ${self.price_stem} per stem."

  def as_dict(self):
    """Returns dictionary version of Flower models"""
    return {
        'id': self.id,
        'name': self.name,
        'color': self.color,
        'img,': self.img,
        'price_stem,': self.price_stem
    }