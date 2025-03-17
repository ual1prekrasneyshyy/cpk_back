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

    def validate(self, attrs):
        if attrs['rating'] > 5.0 or attrs['rating'] < 0.0:
            raise serializers.ValidationError({'rating': 'Rating should be between 0.0 and 5.0!'})
        elif attrs['price'] < 0.0:
            raise serializers.ValidationError({'price': 'Price can not be negative!'})

        check_subcategory = SubCategory.objects.get(pk=attrs['category'])

        if check_subcategory is None:
            raise serializers.ValidationError({'subcategory': 'Subcategory does not exist!'})

        return attrs


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

    def validate(self, attrs):
        check_category = Category.objects.get(pk=attrs['category'])

        if check_category is None:
            raise serializers.ValidationError({'category': 'Category does not exist!'})

        return attrs


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

    def validate(self, attrs):
        check_item = Item.objects.get(pk=attrs['item'])

        if check_item is None:
            raise serializers.ValidationError({'item': 'Item does not exist!'})

        check_cart = Cart.objects.get(pk=attrs['cart'])

        if check_cart is None:
            raise serializers.ValidationError({'cart': 'Cart does not exist!'})


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