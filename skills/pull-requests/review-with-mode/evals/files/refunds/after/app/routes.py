from app.handlers.orders import handle_discount
from app.handlers.refunds import handle_refund

# request["user_id"] is set by the auth middleware from the session, never from the client.
ROUTES = {
    "POST /orders/discount": handle_discount,
    "POST /orders/refund": handle_refund,
}
