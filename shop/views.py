from datetime import datetime
from gc import get_objects
from unicodedata import category

from django.http import JsonResponse
from rest_framework.utils.serializer_helpers import JSONBoundField
from rest_framework.views import APIView

from shop.models import Category, Item, SubCategory, Cart, CartItem
from shop.serializers import ViewCategorySerializer, ViewSubcategorySerializer, \
    SaveSubcategorySerializer, SaveCategorySerializer, SaveItemSerializer, ViewItemSerializer, CartSerializer, \
    CartItemSerializer, SaveCartItemSerializer


# Create your views here.
class CategoryAPI(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = ViewCategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        serializer = SaveCategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class CategoryDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)

        if category:
            serializer = ViewCategorySerializer(category)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)

    def put(self, request, pk):
        category = self.get_object(pk)

        if category is None:
            return JsonResponse({'error': 'Category not found'}, status=404)

        serializer = SaveCategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        category = self.get_object(pk)

        if category:
            category.delete()
            return JsonResponse({'message': 'Category deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)



class SubCategoryAPI(APIView):
    def get(self, request):
        if 'category-id' in request.GET:
            category_id = request.GET.get('category-id')

            subcategories = SubCategory.objects.filter(category_id=category_id)
            serializer = ViewSubcategorySerializer(subcategories, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)

    def post(self, request):
        serializer = SaveSubcategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class SubCategoryDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        subcategory = self.get_object(pk)
        if subcategory:
            serializer = ViewSubcategorySerializer(subcategory)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': 'Subcategory not found'}, status=404)

    def put(self, request, pk):
        subcategory = self.get_object(pk)

        if subcategory is None:
            return JsonResponse({'error': 'Subcategory not found'}, status=404)

        serializer = SaveSubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        subcategory = self.get_object(pk)

        if subcategory:
            subcategory.delete()
            return JsonResponse({'message': 'Subcategory deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Subcategory not found'}, status=404)


class ItemAPI(APIView):
    def get(self, request):
        if 'category-id' in request.GET:
            category_id = request.GET.get('category-id')

            items = Item.objects.filter(category_id=category_id)
            serializer = ViewItemSerializer(items, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)

    def post(self, request):
        serializer = SaveItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class ItemDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return None

    def get(self, request, pk):
        item = self.get_object(pk)
        if item:
            serializer = ViewItemSerializer(item)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)

    def put(self, request, pk):
        item = self.get_object(pk)

        if item is None:
            return JsonResponse({'error': 'Item not found'}, status=404)

        serializer = SaveItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def patch(self, request, pk):
        current_user = request.user

        if current_user.is_authenticated:
            item = Item.objects.get(pk=pk)

            if item in current_user.favourite_items.all():
                current_user.favourite_items.remove(item)
            else:
                current_user.favourite_items.add(item)

            current_user.save()

            return JsonResponse({'message': 'Item favourite status changed'}, status=200)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)




    def delete(self, request, pk):
        item = self.get_object(pk)

        if item:
            item.delete()
            return JsonResponse({'message': 'Item deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)


class CartAPI(APIView):
    def get_object(self, user):
        cart = Cart.objects.filter(user=user).first()
        return cart

    def get(self, request):
        current_user = request.user

        if current_user.is_authenticated:
            cart = self.get_object(current_user)

            # if cart.empty:
            #     return JsonResponse({'error': 'Cart empty'}, status=404)

            if cart:
                serializer = CartSerializer(cart)
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse({'error': 'Cart not registered'}, status=404)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    def post(self, request):
        current_user = request.user

        if current_user.is_authenticated:
            cart = self.get_object(current_user)

            if cart:
                return JsonResponse({'error': 'Cart has already been registered'}, status=400)

            create_cart = Cart(user=current_user, empty=True)
            create_cart.save()
            return JsonResponse({'message': 'Cart created'}, status=201)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    def patch(self, request):
        current_user = request.user

        if current_user.is_authenticated:
            cart = self.get_object(current_user)

            if cart is None:
                return JsonResponse({'error': 'Cart not registered'}, status=404)

            if not cart.empty:
                return JsonResponse({'error': 'Cart has already been activated'}, status=400)

            cart.empty = False
            cart.started_at = datetime.now()
            cart.save()

            return JsonResponse({'message': 'Cart activated'}, status=200)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    def delete(self, request):
        current_user = request.user

        if current_user.is_authenticated:
            cart = self.get_object(current_user)

            if cart is None:
                return JsonResponse({'error': 'Cart not registered'}, status=404)

            if cart.empty:
                return JsonResponse({'error': 'Cart is not activated'}, status=400)

            cart.empty = True

            for item in cart.items.all():
                item.delete()

            cart.save()
            return JsonResponse({'message': 'Cart refreshed'}, status=200)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)




class AddCartItemAPI(APIView):
    def post(self, request):
        current_user = request.user

        if current_user.is_authenticated:
            serializer = SaveCartItemSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Item has been added to the cart'}, status=201)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)


class ManipulateCartItemAPI(APIView):
    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return None

    def put(self, request, pk):
        current_user = request.user

        if current_user.is_authenticated:
            cart_item = self.get_object(pk)

            if cart_item is None:
                return JsonResponse({'error': 'Item not found'}, status=404)

            serializer = SaveCartItemSerializer(cart_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # return JsonResponse({'message': 'Item quantity has been changed'}, status=200)
                return JsonResponse(serializer.data, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    def delete(self, request, pk):
        current_user = request.user

        if current_user.is_authenticated:
            cart_item = self.get_object(pk)

            if cart_item is None:
                return JsonResponse({'error': 'Item not found'}, status=404)

            cart_item.delete()
            return JsonResponse({'message': 'Item deleted from the cart'}, status=200)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)