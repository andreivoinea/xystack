"""Listing endpoint for the product catalogue."""

from catalogue import all_products
from paginate import get_page, page_count

PER_PAGE = 20


def list_products(request):
    products = all_products()
    page = int(request.get("page", 1))
    return {
        "status": 200,
        "items": get_page(products, page, PER_PAGE),
        "pages": page_count(len(products), PER_PAGE),
    }
