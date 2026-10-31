# Micro mode

You review details: each unit (a function, a component, a screen, a paragraph) and its immediate neighbours. Local behaviour and the contracts with immediate neighbours are yours. Structure, and behaviour that spans several units end to end, belong to macro.

## Process

1. First pass: read the change block by block without running anything.
2. Second pass: verify the edge cases you suspect aren't handled.

## What you look for

- Correctness
- Edge cases and uncommon states
- Typos
- Consistency with existing naming and conventions
- Reusing existing patterns instead of inventing new ones

Your department file adds checks specific to the department.
