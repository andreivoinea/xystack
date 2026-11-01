"""Split lists into pages for the listing endpoints."""


def page_count(total, per_page):
    """Return how many pages are needed to show `total` items."""
    if per_page <= 0:
        raise ValueError("per_page must be positive")
    return (total + per_page - 1) // per_page


def get_page(items, page, per_page):
    """Return the items on `page`. Pages are numbered from 1."""
    if per_page <= 0:
        raise ValueError("per_page must be positive")
    if page < 1:
        raise ValueError("page must be 1 or more")
    start = page * per_page
    return items[start:start + per_page]
