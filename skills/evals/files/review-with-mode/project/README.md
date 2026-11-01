# orders-api

Order handling for the shop backend.

## Layout

- `src/handlers/`: turn HTTP requests into service calls and map errors to status codes.
- `src/services/`: business rules. The only code allowed to import `src/db.ts`.
- `src/db.ts`: storage, a JSON file at `$ORDERS_DB` (default `data/orders.json`).
- `src/money.ts`: money parsing and formatting. Never use floating-point maths for money.
- `scripts/`: maintenance scripts, run from the repository root.
- `architecture/workspace.dsl`: the C4 model. Keep it current when you add or change components or their relationships.

## Development

```sh
npm install
npm test          # run the tests
scripts/check.sh  # what CI runs
```
