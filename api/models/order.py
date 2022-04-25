from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Order(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  
  name= models.CharField(max_length=100)
  size= models.CharField(max_length=100)
  price_range = models.CharField(max_length=100)
  color = models.CharField(max_length=100)
  flower = models.ForeignKey('Flower', on_delete=models.CASCADE)
  vase = models.CharField(max_length=100)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The order named '{self.name}' is {self.color} in color."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'name': self.name,
        'size': self.size,
        'price_range': self.price_range,
        'color': self.color,
        'vase': self.vase_mat
    }
