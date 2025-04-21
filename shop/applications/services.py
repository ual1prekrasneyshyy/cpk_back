from shop.domain.repositories import CartItemRepository, CategoryRepository, SubCategoryRepository, ItemRepository, \
    CartRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository


class SubCategoryService:
    def __init__(self, repository: SubCategoryRepository):
        self.repository = repository


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository


class CartService:
    def __init__(self, repository: CartRepository):
        self.repository = repository


class CartItemService:
    def __init__(self, repository: CartItemRepository):
        self.repository = repository