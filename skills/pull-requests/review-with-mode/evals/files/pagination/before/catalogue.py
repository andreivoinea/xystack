"""Product catalogue."""

PRODUCTS = [{"id": n, "name": f"Product {n}"} for n in range(1, 46)]


def all_products():
    return list(PRODUCTS)
