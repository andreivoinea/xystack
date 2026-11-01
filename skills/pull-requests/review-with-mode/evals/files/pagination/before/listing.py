"""Listing endpoint for the product catalogue."""

from catalogue import all_products


def list_products(request):
    return {"status": 200, "items": all_products()}
