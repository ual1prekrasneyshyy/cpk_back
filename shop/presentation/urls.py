from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from shop.presentation.views import CategoryAPI, CategoryDetailAPI, ItemAPI, SubCategoryAPI, SubCategoryDetailAPI, \
    ItemDetailAPI, \
    CartAPI, AddCartItemAPI, ManipulateCartItemAPI, RegisterView, UserDetailView, LogoutView, rate_item

urlpatterns = [
    path('api/categories', CategoryAPI.as_view()),
    path('api/categories/<int:pk>', CategoryDetailAPI.as_view()),
    path('api/sub-categories', SubCategoryAPI.as_view()),
    path('api/sub-categories/<int:pk>', SubCategoryDetailAPI.as_view()),
    path('api/items', ItemAPI.as_view()),
    path('api/items/<int:pk>', ItemDetailAPI.as_view()),
    path('api/items/rate', rate_item),
    path('api/cart', CartAPI.as_view()),
    path('api/cart/item', AddCartItemAPI.as_view()),
    path('api/cart/item/<int:pk>', ManipulateCartItemAPI.as_view()),

    path('auth/register', RegisterView.as_view()),
    path('auth/user', UserDetailView.as_view()),
    path('auth/login', obtain_auth_token),
    path('auth/logout', LogoutView.as_view()),

]