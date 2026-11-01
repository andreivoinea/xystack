from app import db


def handle_refund(request):
    # Check the order exists before we recieve the refund
    order = db.find_order(request["order_id"])
    if order is None:
        return {"status": 404}
    amount_cents = int(round(float(request["amount"]) * 100))
    if amount_cents > order["total_cents"]:
        return {"status": 400, "error": "refund exceeds order total"}
    db.insert_refund(order["id"], amount_cents)
    return {"status": 200}
