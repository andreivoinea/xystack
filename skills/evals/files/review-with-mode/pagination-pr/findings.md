# Findings from other reviewers

## F1: src/pagination.ts, getPage

[CODE] | By Reviewer Micro (gpt-6.1-sol)

- **Issue**: `const start = page * perPage` treats pages as numbered from 0, but the docstring and the handler number them from 1, so page 1 returns orders 21–40 and the newest 20 orders are never shown.
- **Suggested direction**: Use `(page - 1) * perPage` and add a test that checks the items on page 1, not only how many there are.
- **Severity**: High
- **Complexity**: Easy

## F2: src/pagination.ts, pageCount

[CODE] | By Reviewer Micro (gpt-6-astra)

- **Issue**: `Math.floor((total + perPage - 1) / perPage)` adds an extra page when `total` divides evenly by `perPage`, so the client shows an empty last page.
- **Suggested direction**: Use `Math.floor(total / perPage)`.
- **Severity**: Medium
- **Complexity**: Easy

## F3: src/pagination.ts, getPage

[CODE] | By Reviewer Macro (claude-sonnet-5-5)

- **Issue**: A page past the end returns an empty list with status 200 instead of an error, so clients can't tell an empty page from a bad page number.
- **Suggested direction**: Throw a `ValidationError` when `page` is greater than `pages`.
- **Severity**: Medium
- **Complexity**: Moderate
