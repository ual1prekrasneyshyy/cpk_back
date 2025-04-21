from django.contrib.auth.models import User
from rest_framework import serializers



class ViewItemSerializer(serializers.Serializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    rating = serializers.FloatField()
    image_url = serializers.CharField()



class SaveItemSerializer(serializers.Serializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    rating = serializers.FloatField()
    image_url = serializers.CharField()
    category = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['rating'] > 5.0 or attrs['rating'] < 0.0:
            raise serializers.ValidationError({'rating': 'Rating should be between 0.0 and 5.0!'})
        elif attrs['price'] < 0.0:
            raise serializers.ValidationError({'price': 'Price can not be negative!'})

        return attrs


class ViewSubcategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    image_url = serializers.CharField()


class SaveSubcategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    image_url = serializers.CharField()
    category = serializers.IntegerField()


class ViewCategorySerializer(serializers.Serializer):
    subcategories = ViewSubcategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    image_url = serializers.CharField()


class SaveCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    image_url = serializers.CharField()


class SaveCartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    item = serializers.IntegerField()
    cart = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CartItemSerializer(serializers.Serializer):
    item = ViewItemSerializer(read_only=True)
    quantity = serializers.IntegerField()


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    started_at = serializers.DateTimeField()
    empty = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):
    favourite_items = ViewItemSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'favourite_items']
        read_only_fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 're_password', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({'password': 'Password does not match!'})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        return user