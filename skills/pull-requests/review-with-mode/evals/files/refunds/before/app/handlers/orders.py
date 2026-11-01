from app.services import orders


def handle_discount(request):
    try:
        order = orders.apply_discount(request["order_id"], request["user_id"], request["amount"])
    except orders.OrderNotFound:
        return {"status": 404}
    return {"status": 200, "order": order}
