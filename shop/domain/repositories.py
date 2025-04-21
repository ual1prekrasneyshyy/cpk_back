from abc import ABC, abstractmethod

from shop.domain.entities import Category, SubCategory, Item, Cart, CartItem


class CategoryRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Category]:
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Category:
        pass

    @abstractmethod
    def save(self, category: Category) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, category_id: int) -> None:
        pass


class SubCategoryRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[SubCategory]:
        pass

    @abstractmethod
    def get_by_id(self, subcategory_id: int) -> SubCategory:
        pass

    @abstractmethod
    def save(self, subcategory: SubCategory) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, subcategory_id: int) -> None:
        pass


class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Item]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Item:
        pass

    @abstractmethod
    def save(self, item: Item) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, item_id: int) -> None:
        pass


class CartRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Cart]:
        pass

    @abstractmethod
    def get_by_id(self, cart_id: int) -> Cart:
        pass

    @abstractmethod
    def save(self, cart: Cart) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, cart_id: int) -> None:
        pass


class CartItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[CartItem]:
        pass

    @abstractmethod
    def get_by_id(self, cart_item_id: int) -> CartItem:
        pass

    @abstractmethod
    def save(self, cart_item: CartItem) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, cart_item_id: int) -> None:
        pass