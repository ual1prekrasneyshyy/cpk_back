from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from shop.applications.services import CategoryService, SubCategoryService, ItemService
from shop.domain.entities import Category, Item, SubCategory, Cart, CartItem
from shop.domain.repositories import CategoryRepository, SubCategoryRepository, ItemRepository
from shop.infrastructure.models import CartModel, CartItemModel, ItemModel
from shop.infrastructure.repositories import DjangoCategoryRepository, DjangoSubCategoryRepository, DjangoItemRepository
from shop.infrastructure.serializers import ViewCategorySerializer, ViewSubcategorySerializer, \
    SaveSubcategorySerializer, SaveCategorySerializer, SaveItemSerializer, ViewItemSerializer, CartSerializer, \
    SaveCartItemSerializer, RegisterSerializer, UserSerializer


# Create your views here.
class CategoryAPI(APIView):
    def get(self, request):
        repository = DjangoCategoryRepository()
        service = CategoryService(repository)
        categories = repository.get_all()
        serializer = ViewCategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        serializer = SaveCategorySerializer(data=request.data)

        if serializer.is_valid():
            repository = DjangoCategoryRepository()
            service = CategoryService(repository)
            repository.save(serializer.validated_data)
            return JsonResponse({'message': 'Category created!'}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class CategoryDetailAPI(APIView):
    def get(self, request, pk):
        repository = DjangoCategoryRepository()
        service = CategoryService(repository)
        category = repository.get_by_id(pk)

        if category:
            serializer = ViewCategorySerializer(category)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)

    def put(self, request, pk):
        repository = DjangoCategoryRepository()
        service = CategoryService(repository)
        category = repository.get_by_id(pk)

        if category is None:
            return JsonResponse({'error': 'Category not found'}, status=404)

        serializer = SaveCategorySerializer(category, data=request.data)

        if serializer.is_valid():
            repository.save(serializer.validated_data)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        repository = DjangoCategoryRepository()
        service = CategoryService(repository)
        category = repository.get_by_id(pk)

        if category:
            repository.delete_by_id(pk)
            return JsonResponse({'message': 'Category deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)


class SubCategoryAPI(APIView):
    def get(self, request):
        if 'category-id' in request.GET:
            category_id = request.GET.get('category-id')

            repository = DjangoSubCategoryRepository()
            service = SubCategoryService(repository)
            subcategories = repository.get_all()
            serializer = ViewSubcategorySerializer(subcategories, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)

    def post(self, request):
        serializer = SaveSubcategorySerializer(data=request.data)

        if serializer.is_valid():
            repository = DjangoSubCategoryRepository()
            service = SubCategoryService(repository)
            repository.save(serializer.validated_data)
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class SubCategoryDetailAPI(APIView):
    def get(self, request, pk):
        repository = DjangoSubCategoryRepository()
        service = SubCategoryService(repository)
        # service = CategoryService(repository)
        subcategory = repository.get_by_id(pk)
        if subcategory:
            serializer = ViewSubcategorySerializer(subcategory)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': 'Subcategory not found'}, status=404)

    def put(self, request, pk):
        repository = DjangoSubCategoryRepository()
        service = SubCategoryService(repository)
        subcategory = repository.get_by_id(pk)

        if subcategory is None:
            return JsonResponse({'error': 'Subcategory not found'}, status=404)

        serializer = SaveSubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            repository.save(serializer.validated_data)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        repository = DjangoSubCategoryRepository()
        service = SubCategoryService(repository)
        subcategory = repository.get_by_id(pk)

        if subcategory:
            repository.delete_by_id(pk)
            return JsonResponse({'message': 'Subcategory deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Subcategory not found'}, status=404)


class ItemAPI(APIView):
    def get(self, request):
        if 'category-id' in request.GET:
            category_id = request.GET.get('category-id')

            repository = DjangoItemRepository()
            service = ItemService(repository)

            items = repository.get_all()
            serializer = ViewItemSerializer(items, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Category not found'}, status=404)

    def post(self, request):
        repository = DjangoItemRepository()
        service = ItemService(repository)
        serializer = SaveItemSerializer(data=request.data)
        if serializer.is_valid():
            repository.save(serializer.validated_data)
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class ItemDetailAPI(APIView):
    def get(self, request, pk):

        repository = DjangoItemRepository()
        service = ItemService(repository)
        item = repository.get_by_id(pk)
        if item:
            serializer = ViewItemSerializer(item)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)

    def put(self, request, pk):
        repository = DjangoItemRepository()
        service = ItemService(repository)
        item = repository.get_by_id(pk)

        if item is None:
            return JsonResponse({'error': 'Item not found'}, status=404)

        serializer = SaveItemSerializer(item, data=request.data)
        if serializer.is_valid():
            repository.save(serializer.validated_data)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def patch(self, request, pk):
        current_user = request.user

        if current_user.is_authenticated:
            repository = DjangoItemRepository()
            service = ItemService(repository)
            item = repository.get_by_id(pk)

            if item in current_user.favourite_items.all():
                current_user.favourite_items.remove(item)
            else:
                current_user.favourite_items.add(item)

            current_user.save()

            return JsonResponse({'message': 'Item favourite status changed'}, status=200)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    def delete(self, request, pk):
        repository = DjangoItemRepository()
        service = ItemService(repository)
        item = repository.get_by_id(pk)

        if item:
            repository.delete_by_id(pk)
            return JsonResponse({'message': 'Item deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)


class CartAPI(APIView):
    def get_object(self, user):
        cart = CartModel.objects.filter(user=user).first()
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

            create_cart = CartModel(user=current_user, empty=True)
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
            return CartItemModel.objects.get(pk=pk)
        except CartItemModel.DoesNotExist:
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



# Create your views here.
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # Allow anyone to register
    serializer_class = RegisterSerializer


class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can see/edit their credentials

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response({'message': 'You have successfully logged out!'}, status=200)


@csrf_exempt #temporal
def rate_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('id')
        mark = data.get('mark')

        if mark < 0 or mark > 5:
            return JsonResponse({'error': 'Mark can not be negative or more that 5'})

        item = ItemModel.objects.get(pk=item_id)
        rates = []

        if item.rates:
            rates = item.rates

        rates.append(mark)
        item.rates = rates

        s = 0

        for rate in item.rates:
            s += rate

        item.rating = s / len(item.rates)

        item.save()

        return JsonResponse({'message': 'Item rated'})