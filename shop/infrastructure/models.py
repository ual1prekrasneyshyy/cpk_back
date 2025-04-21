import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


# Create your models here.
class CategoryModel(models.Model):
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


class SubCategoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        db_table = 'sub_categories'

    def __str__(self):
        return self.name


class ItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.TextField()
    price = models.IntegerField()
    rating = models.FloatField()
    quantity = models.IntegerField()
    category = models.ForeignKey(SubCategoryModel, on_delete=models.CASCADE, related_name='items')
    lovers = models.ManyToManyField(User, related_name='favourite_items')


    # additional field
    rates = models.JSONField(
        null=True,
        blank=True,
        default=list
    )

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        db_table = 'items'

    def __str__(self):
        return f'{self.name}: {self.description}'


class CartModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    started_at = models.DateTimeField(default=timezone.now)
    empty = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = 'carts'


class CartItemModel(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'
        db_table = 'cart_items'


