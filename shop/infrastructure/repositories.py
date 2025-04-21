from shop.domain.repositories import CategoryRepository, SubCategoryRepository, ItemRepository, CartItemRepository, \
    CartRepository
from shop.domain.entities import Category, SubCategory, Item, CartItem, Cart
from shop.infrastructure.mappers import category_model_to_entity, category_entity_to_model, \
    sub_category_model_to_entity, sub_category_entity_to_model, item_model_to_entity, item_entity_to_model, \
    cart_item_model_to_entity, cart_item_entity_to_model, cart_model_to_entity, cart_entity_to_model
from shop.infrastructure.models import CategoryModel, SubCategoryModel, ItemModel, CartItemModel, CartModel


class DjangoCategoryRepository(CategoryRepository):
    def get_all(self) -> list[Category]:
        category_model_list = CategoryModel.objects.all()
        category_entity_list = []

        for category_model in category_model_list:
            category_entity_list.append(category_model_to_entity(category_model))

        return category_entity_list

    def get_by_id(self, category_id: int) -> Category:
        category_model = CategoryModel.objects.get(pk=category_id)

        if category_model:
            return category_model_to_entity(category_model)
        else:
            return None

    def save(self, category: Category) -> None:
        category_entity_to_model(category).save()


    def delete_by_id(self, category_id: int) -> None:
        CategoryModel.objects.get(pk=category_id).delete()


class DjangoSubCategoryRepository(SubCategoryRepository):
    def get_all(self) -> list[SubCategory]:
        subcategory_model_list = SubCategoryModel.objects.all()
        subcategory_entity_list = []

        for subcategory_model in subcategory_model_list:
            subcategory_entity_list.append(sub_category_model_to_entity(subcategory_model))

        return subcategory_entity_list

    def get_by_id(self, sub_category_id: int) -> SubCategory:
        sub_category_model = SubCategoryModel.objects.get(pk=sub_category_id)

        if sub_category_model:
            return sub_category_model_to_entity(sub_category_model)
        else:
            return None

    def save(self, sub_category: SubCategory) -> None:
        sub_category_entity_to_model(sub_category).save()


    def delete_by_id(self, sub_category_id: int) -> None:
        SubCategoryModel.objects.get(pk=sub_category_id).delete()


class DjangoItemRepository(ItemRepository):
    def get_all(self) -> list[Item]:
        item_model_list = ItemModel.objects.all()
        item_entity_list = []

        for item_model in item_model_list:
            item_entity_list.append(item_model_to_entity(item_model))

        return item_entity_list

    def get_by_id(self, item_id: int) -> Item:
        item_model = ItemModel.objects.get(pk=item_id)

        if item_model:
            return item_model_to_entity(item_model)
        else:
            return None

    def save(self, item: Item) -> None:
        item_entity_to_model(item).save()

    def delete_by_id(self, item_id: int) -> None:
        ItemModel.objects.get(pk=item_id).delete()


class DjangoCartRepository(CartRepository):
    def get_all(self) -> list[Cart]:
        cart_model_list = CartModel.objects.all()
        cart_entity_list = []

        for cart_model in cart_model_list:
            cart_entity_list.append(cart_model_to_entity(cart_model))

        return cart_entity_list

    def get_by_id(self, cart_id: int) -> Cart:
        cart_model = CartModel.objects.get(pk=cart_id)

        if cart_model:
            return cart_model_to_entity(cart_model)
        else:
            return None

    def save(self, cart: Cart) -> None:
        cart_entity_to_model(cart).save()

    def delete_by_id(self, cart_id: int) -> None:
        CartModel.objects.get(pk=cart_id).delete()


class DjangoCartItemRepository(CartItemRepository):
    def get_all(self) -> list[CartItem]:
        cart_item_model_list = CartItemModel.objects.all()
        cart_item_entity_list = []

        for cart_item_model in cart_item_model_list:
            cart_item_entity_list.append(cart_item_model_to_entity(cart_item_model))

        return cart_item_entity_list

    def get_by_id(self, cart_item_id: int) -> CartItem:
        cart_item_model = CartItemModel.objects.get(pk=cart_item_id)

        if cart_item_model:
            return cart_item_model_to_entity(cart_item_model)
        else:
            return None

    def save(self, cart_item: CartItem) -> None:
        cart_item_entity_to_model(cart_item).save()

    def delete_by_id(self, cart_item_id: int) -> None:
        CartItemModel.objects.get(pk=cart_item_id).delete()