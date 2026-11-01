# orders-api

Order handling for the shop backend.

## Layout

- `src/handlers/`: turn HTTP requests into service calls and map errors to status codes.
- `src/services/`: business rules. The only code allowed to import `src/db.ts`.
- `src/db.ts`: storage.
- `src/money.ts`: money parsing and formatting. Never use floating-point maths for money.
- `scripts/`: maintenance scripts, run from the repository root.

## Development

```sh
npm install
npm test          # run the tests
scripts/check.sh  # what CI runs
```
