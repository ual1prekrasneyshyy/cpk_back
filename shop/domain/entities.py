from dataclasses import dataclass
from typing import Optional
from datetime import datetime as dt


@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    # favourite_items: list[Item]
    # cart: Cart


@dataclass
class Category:
    id: Optional[int]
    name: str
    description: str
    image_url: str

    def __str__(self):
        return self.name


@dataclass
class SubCategory:
    id: Optional[int]
    name: str
    description: str
    image_url: str
    category: Category

    def __str__(self):
        return self.name


@dataclass
class Item:
    id: Optional[int]
    name: str
    description: str
    image_url: str
    price: int
    rating: float
    quantity: int
    category: SubCategory
    lovers: list[User]

    # additional field
    rates: list[int]

    def __str__(self):
        return f'{self.name}: {self.description}'


@dataclass
class Cart:
    id: Optional[int]
    user: User
    started_at: dt
    empty: bool


@dataclass
class CartItem:
    id: Optional[int]
    cart: Cart
    item: Item
    quantity: int
