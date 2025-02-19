from rest_framework import serializers
#
from shop.models import Category, Item, SubCategory, Cart, CartItem


class ViewItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price', 'rating', 'image_url', 'category_name')
        read_only_fields = ['id']


class SaveItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'price', 'rating', 'image_url', 'category', 'category_name')
        read_only_fields = ['id']






class ViewSubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'description', 'image_url', 'category_name')
        read_only_fields = ['id']


class SaveSubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'description', 'image_url', 'category', 'category_name')
        read_only_fields = ['id']





class ViewCategorySerializer(serializers.ModelSerializer):
    subcategories = ViewSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'image_url', 'subcategories')
        read_only_fields = ['id']


class SaveCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'image_url')
        read_only_fields = ['id']


class SaveCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'item', 'cart', 'quantity']
        read_only_fields = ['id']


class CartItemSerializer(serializers.ModelSerializer):
    item = ViewItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['item', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'started_at', 'empty']