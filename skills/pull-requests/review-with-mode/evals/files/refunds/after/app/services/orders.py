from app import db
from app.services.money import to_cents


class OrderNotFound(Exception):
    pass


def get_order_for_user(order_id, user_id):
    """Return the order if it belongs to the user. Other users' orders look missing."""
    order = db.find_order(order_id)
    if order is None or order["user_id"] != user_id:
        raise OrderNotFound(order_id)
    return order


def apply_discount(order_id, user_id, amount):
    order = get_order_for_user(order_id, user_id)
    order["total_cents"] -= to_cents(amount)
    return order
