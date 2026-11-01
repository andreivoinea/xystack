# Findings from other reviewers

## F1: paginate.py, get_page

[CODE] | By Reviewer Micro (gpt-6.1-sol)

- **Issue**: `start = page * per_page` treats pages as numbered from 0, but the docstring and `listing.py` number them from 1, so page 1 returns the second page and the first 20 products are never shown.
- **Suggested direction**: Use `start = (page - 1) * per_page` and add a test for page 1.
- **Severity**: High
- **Complexity**: Easy

## F2: paginate.py, page_count

[CODE] | By Reviewer Micro (gpt-6-astra)

- **Issue**: `(total + per_page - 1) // per_page` adds an extra page when `total` divides evenly by `per_page`, so the listing shows an empty last page.
- **Suggested direction**: Use `total // per_page`.
- **Severity**: Medium
- **Complexity**: Easy

## F3: paginate.py, get_page

[CODE] | By Reviewer Macro (claude-sonnet-5-5)

- **Issue**: A page past the end returns an empty list instead of an error, so clients can't tell an empty page from a bad page number.
- **Suggested direction**: Raise `ValueError` when `page` is greater than `page_count`.
- **Severity**: Medium
- **Complexity**: Moderate
