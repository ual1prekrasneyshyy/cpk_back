from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.TextField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        db_table = 'sub_categories'


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.TextField()
    price = models.IntegerField()
    rating = models.FloatField()
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='items')
    lovers = models.ManyToManyField(User, related_name='favourite_items')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        db_table = 'items'

    def __str__(self):
        return f'{self.name}: {self.description}'


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    started_at = models.DateTimeField(default=datetime.now())
    empty = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = 'carts'


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'
        db_table = 'cart_items'


