# Code

## Verifying

Run the code, write a throwaway test, or check types and behaviour against the docs. Follow the shared verification safeguards for any throwaway tests or generated artifacts. Never run the change against production or shared services.

## Severity examples

- **Low**: naming, formatting, style
- **Medium**: an unlikely edge case returns a wrong result
- **High**: a common path fails for some users or inputs
- **Critical**: widespread outages, irreversible data loss, or security vulnerabilities with severe impact

## Micro checks

- Typos in identifiers, strings, and comments
- Off-by-one errors, empty and null inputs, boundaries
- Error handling and cleanup on failure paths
- Tests: significant new behaviour and bug fixes have appropriate regression coverage; report material gaps with a concrete failure scenario
- Concurrency and ordering issues within the unit
- Functional style where the project uses it
- Reusing existing helpers instead of writing new ones

## Macro checks

- Module boundaries and dependency direction
- Public interfaces and backwards compatibility
- Data flow and where state lives
- Performance at the scale the project runs at
- Security boundaries: untrusted input, secrets, permissions, and how the change affects them
- Architecture: Structurizr C4 diagrams. New projects should establish them, and changes that add or alter components or relationships should keep them current. Flag gaps the change introduces or worsens, not unrelated older ones
