from django.db import models
from django.contrib.auth import get_user_model
from .order import Order
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Inquiry(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/

  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone_number = models.CharField(max_length=11)
  email = models.CharField(max_length=255)
  comment = models.CharField(max_length=250)
  order = models.ForeignKey(
    'Order',
    on_delete=models.CASCADE,
    null=False,
    related_name='order_id'
  )
  est_price = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The order named '{self.order}' was submited at {self.created_at}."

  def as_dict(self):
    """Returns dictionary version of Order models"""
    return {
        'id': self.id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'phone_number': self.phone_number,
        'email': self.email,
        'comment': self.comment,
        'order': self.order,
        'est_price': self.est_price,
        'created_at': self.created_at,
    }
