# Add paginated order history

Customers with many orders were getting their whole history in one response, which made the orders page slow.

- Adds `GET /orders?page=N`, 20 orders per page, newest first. Pages are numbered from 1.
- Adds `src/pagination.ts` so other listings can reuse it.
- Adds `scripts/export-orders.sh` for the monthly finance export.
