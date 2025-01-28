import json
from concurrent.futures import ThreadPoolExecutor
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        """Load Cart from dictionary."""
        contents = json.loads(data['contents'])  # Safely parse the contents as a JSON string
        return Cart(data['id'], data['username'], contents, data['cost'])


def fetch_product(product_id: int) -> Product:
    """Helper function to fetch a product by ID."""
    return products.get_product(product_id)


def get_cart(username: str) -> list[Product]:
    """Get the cart for a user."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        # Directly parse the 'contents' field if it's in string format (like JSON)
        try:
            contents = json.loads(cart_detail['contents'])
        except (TypeError, json.JSONDecodeError):
            contents = []

        for content in contents:
            items.append(content)

    # Use threading to fetch products concurrently
    with ThreadPoolExecutor() as executor:
        products_list = list(executor.map(fetch_product, items))
    
    return products_list


def add_to_cart(username: str, product_id: int) -> None:
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """Delete the user's entire cart."""
    dao.delete_cart(username)


# Checkout Process - Optimized Version
def checkout(cart: list[Product]) -> float:
    """Checkout process to calculate total cost."""
    total = sum(item.cost for item in cart)  # Directly sum the costs
    return total
