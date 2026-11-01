# Add refunds endpoint

Support has been issuing refunds by editing the database by hand. This adds an endpoint for customers to refund their own paid orders.

- Adds `POST /orders/:id/refund` with an `amount`; partial refunds are allowed.
- Records each refund and marks the order refunded.
