from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


class Item(Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'наименование товара'

class Order(Model):
    datetime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)
    items = models.ManyToManyField(Item, through="OrderItems")

class OrderItems(Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    count = models.PositiveSmallIntegerField(default=1)


class Discount(Model):
    discount_size = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
