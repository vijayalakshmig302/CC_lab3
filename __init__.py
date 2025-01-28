import asyncio
from concurrent.futures import ThreadPoolExecutor
from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> 'Product':
        """Load a Product instance from data."""
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


async def fetch_product_async(product_id: int) -> Product:
    """Asynchronously fetch a product by its ID."""
    product_data = await dao.get_product_async(product_id)  # Assume async version of `dao.get_product`
    return Product.load(product_data)


async def list_products() -> list[Product]:
    """Asynchronously list all products."""
    products = await dao.list_products_async()  # Assume async version of `dao.list_products`
    return [Product.load(product) for product in products]


async def get_product(product_id: int) -> Product:
    """Fetch a product asynchronously."""
    return await fetch_product_async(product_id)


async def add_product(product: dict):
    """Add a product to the database."""
    await dao.add_product_async(product)  # Assume async version of `dao.add_product`


async def update_qty(product_id: int, qty: int):
    """Update the quantity of a product asynchronously."""
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    await dao.update_qty_async(product_id, qty)  # Assume async version of `dao.update_qty`


# Optimized version of getting a list of products concurrently
def get_products_concurrently(product_ids: list[int]) -> list[Product]:
    """Fetch products concurrently."""
    with ThreadPoolExecutor() as executor:
        products = list(executor.map(fetch_product_async, product_ids))
    return products
