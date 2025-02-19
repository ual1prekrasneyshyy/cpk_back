from django.urls import path

from shop.views import CategoryAPI, CategoryDetailAPI, ItemAPI, SubCategoryAPI, SubCategoryDetailAPI, ItemDetailAPI, \
    CartAPI, AddCartItemAPI, ManipulateCartItemAPI

urlpatterns = [
    path('categories', CategoryAPI.as_view()),
    path('categories/<int:pk>', CategoryDetailAPI.as_view()),
    path('sub-categories', SubCategoryAPI.as_view()),
    path('sub-categories/<int:pk>', SubCategoryDetailAPI.as_view()),
    path('items', ItemAPI.as_view()),
    path('items/<int:pk>', ItemDetailAPI.as_view()),
    path('cart', CartAPI.as_view()),
    path('cart/item', AddCartItemAPI.as_view()),
    path('cart/item/<int:pk>', ManipulateCartItemAPI.as_view()),
]