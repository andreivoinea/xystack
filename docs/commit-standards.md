# Commit Standards

Commit messages in this repository follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/#specification), with two changes:

1. The allowed types also include the ones from [`@commitlint/config-conventional`](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional).
2. Breaking changes use the `BREAKING CHANGE` type. The `!` marker and the `BREAKING CHANGE:` footer are not used.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Use for |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that don't affect meaning (white-space, formatting, missing semicolons, etc.) |
| `refactor` | A change that neither fixes a bug nor adds a feature |
| `perf` | A change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `build` | Changes to the build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Other changes that don't modify source or test files |
| `revert` | Reverts a previous commit |
| `BREAKING CHANGE` | A change that breaks existing behaviour or interfaces, of any kind |

## Specification

1. Commits MUST be prefixed with a type, which consists of one of the types listed above, followed by the OPTIONAL scope, and a REQUIRED terminal colon and space.
2. The type `feat` MUST be used when a commit adds a new feature, unless the feature is a breaking change.
3. The type `fix` MUST be used when a commit represents a bug fix, unless the fix is a breaking change.
4. A scope MAY be provided after a type. A scope MUST consist of a noun describing a section of the codebase surrounded by parentheses, e.g., `fix(parser):`
5. A description MUST immediately follow the colon and space after the type/scope prefix. The description is a short summary of the change, e.g., `fix: array parsing issue when multiple spaces were contained in string`.
6. A longer commit body MAY be provided after the short description, providing additional contextual information about the change. The body MUST begin one blank line after the description.
7. A commit body is free-form and MAY consist of any number of newline-separated paragraphs.
8. One or more footers MAY be provided one blank line after the body. Each footer MUST consist of a word token, followed by either a `:<space>` or `<space>#` separator, followed by a string value (this is inspired by the [git trailer convention](https://git-scm.com/docs/git-interpret-trailers)).
9. A footer's token MUST use `-` in place of whitespace characters, e.g., `Acked-by` (this helps differentiate the footer section from a multi-paragraph body).
10. A footer's value MAY contain spaces and newlines, and parsing MUST terminate when the next valid footer token/separator pair is observed.
11. Breaking changes MUST use the `BREAKING CHANGE` type, e.g., `BREAKING CHANGE(api): remove v1 endpoints`. This applies whatever else the change does: a breaking feature, fix, refactor, or any other change uses `BREAKING CHANGE`, not its usual type.
12. A `BREAKING CHANGE` commit SHOULD include a body that describes what breaks and how to migrate.
13. Commits MUST NOT use `!` after the type or scope.
14. Commits MUST NOT use a `BREAKING CHANGE` or `BREAKING-CHANGE` footer.
15. Types other than those listed above MUST NOT be used.
16. Types and scopes MUST be lowercase, except the `BREAKING CHANGE` type, which MUST be uppercase. Footer tokens are case-insensitive.

## Examples

A feature with a scope:

```
feat(skills): add review-with-mode skill
```

Documentation only:

```
docs: add commit standards
```

A breaking change with a body:

```
BREAKING CHANGE(installer): rename skills install command to skills add

The `xystack skills install` command is now `xystack skills add`.
Update any scripts that call the old name.
```

A revert with a footer:

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Tooling note

`@commitlint/config-conventional` rejects the `BREAKING CHANGE` type, because its type must be a lowercase word from its list. If commitlint is added to this repository, extend its `type-enum` with `BREAKING CHANGE` and relax `type-case` for that type.
