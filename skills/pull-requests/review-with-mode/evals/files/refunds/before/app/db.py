"""In-memory storage. Only the services package should use this module."""

ORDERS = {}  # order_id -> {"id", "user_id", "total_cents", "status"}
REFUNDS = []


def find_order(order_id):
    return ORDERS.get(order_id)


def insert_refund(order_id, amount_cents):
    REFUNDS.append({"order_id": order_id, "amount_cents": amount_cents})
