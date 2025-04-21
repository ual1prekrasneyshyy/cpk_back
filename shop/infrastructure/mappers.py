from shop.domain.entities import Category, SubCategory, Item, Cart, CartItem
from shop.infrastructure.models import CategoryModel, SubCategoryModel, ItemModel, CartModel, CartItemModel
from django.contrib.auth.models import User as UserModel
from shop.domain.entities import User as UserEntity

def category_entity_to_model(category: Category) -> CategoryModel:
    return CategoryModel(
        id=category.id,
        name=category.name,
        description=category.description,
        image_url=category.image_url,
    )


def category_model_to_entity(category: CategoryModel) -> Category:
    return Category(
        id=category.id,
        name=category.name,
        description=category.description,
        image_url=category.image_url,
    )


def sub_category_entity_to_model(sub_category: SubCategory) -> SubCategoryModel:
    return SubCategoryModel(
        id=sub_category.id,
        name=sub_category.name,
        description=sub_category.description,
        category=category_entity_to_model(sub_category.category),
        image_url=sub_category.image_url,
    )


def sub_category_model_to_entity(sub_category: SubCategoryModel) -> SubCategory:
    return SubCategory(
        id=sub_category.id,
        name=sub_category.name,
        description=sub_category.description,
        category=category_model_to_entity(sub_category.category),
        image_url=sub_category.image_url,
    )


def item_entity_to_model(item: Item) -> ItemModel:
    lover_model_list = []

    for lover in item.lovers:
        lover_model_list.append(user_entity_to_model(lover))

    return ItemModel(
        id=item.id,
        name=item.name,
        description=item.description,
        image_url=item.image_url,
        price=item.price,
        quantity=item.quantity,
        category=sub_category_entity_to_model(item.category),
        rating=item.rating,
        lovers=lover_model_list,
        rates=item.rates,
    )


def item_model_to_entity(item: ItemModel) -> Item:
    lovers_list = []

    for lover in item.lovers.all():
        lovers_list.append(user_model_to_entity(lover))

    return Item(
        id=item.id,
        name=item.name,
        description=item.description,
        image_url=item.image_url,
        price=item.price,
        quantity=item.quantity,
        category=sub_category_model_to_entity(item.category),
        rating=item.rating,
        lovers=lovers_list,
        rates=item.rates or []
    )


def cart_entity_to_model(cart: Cart) -> CartModel:
    return CartModel(
        id=cart.id,
        user=user_model_to_entity(cart.user),
        started_at=cart.started_at,
        empty=cart.empty,
    )


def cart_model_to_entity(cart: CartModel) -> Cart:
    return Cart(
        id=cart.id,
        user=user_entity_to_model(cart.user),
        started_at=cart.started_at,
        empty=cart.empty,
    )


def cart_item_entity_to_model(item: CartItem) -> CartItemModel:
    return CartItemModel(
        id=item.id,
        cart=cart_entity_to_model(item.cart),
        item=item_entity_to_model(item.item),
        quantity=item.quantity,
    )


def cart_item_model_to_entity(item: CartItemModel) -> CartItem:
    return CartItem(
        id=item.id,
        cart=cart_model_to_entity(item.cart),
        item=item_model_to_entity(item.item),
        quantity=item.quantity,
    )

def user_entity_to_model(user: UserEntity) -> UserModel:
    item_model_list = []

    # for item in user.favourite_items:
    #     item_model_list.append(item_entity_to_model(item))

    return UserModel(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        favourite_items=item_model_list,
        cart=None
    )

def user_model_to_entity(user: UserModel) -> UserEntity:
    item_entity_list = []

    for item in user.favourite_items:
        item_entity_list.append(item_model_to_entity(item))

    return UserEntity(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        # favourite_items=item_entity_list,
        password=user.password,
        # cart=None
    )