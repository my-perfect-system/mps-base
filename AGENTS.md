# AGENTS.md — mps-base

Anchor collection for the `mps.*` ecosystem. Hosts shared conventions,
the per-user identity data model (`mps.base.identity`), and shared
helpers (`mps.base.assert_debian13`). All leaves depend on this.

## Galaxy

- **namespace**: `mps`
- **name**: `base`
- **version**: `0.3.1`
- **dependencies**: none (this is the anchor)

## Roles

| Role | Description | Complexity |
|---|---|---|
| `mps.base.identity` | Shared per-user identity model. Produces `identity_users_resolved`, `identity_users_present`, `identity_users_absent`, `identity_user_groups` for every dependent role. | 3 |
| `mps.base.assert_debian13` | Fail-fast assertion that the target host runs Debian 13 (trixie). Declared as a `meta/main.yml` dependency by every role that requires Debian 13. | 1 |

## Filter plugins

`filter_plugins/mps_filter_users.py` — three small functions:

| Filter | Purpose |
|---|---|
| `mps_filter_users(users, role_key, state='present')` | Used by every per-user role to iterate only the users that opted into a specific `user_roles.<key>` flag. Skips empty dicts internally. |
| `mps_resolve_users(users_list, users_catalog)` | Resolves raw `users_list` entries against `users_catalog` to produce `identity_users_resolved`. Replaces the heavy Jinja data-shaping block that previously lived in `roles/identity/tasks/main.yml`. |
| `mps_user_groups(users)` | Flat, deduplicated list of all group names referenced by each user's `group` and `groups` fields. |

All three are unit-testable from plain Python (no Ansible required).

## Conventions

- **Per-user roles disabled by default** — opt in via `user_roles.<key>: true` in the catalog entry.
- **Identity model is the canonical source of truth** — per-user roles filter `identity_users_resolved` inline; no per-role `resolve.yml`.
- **Task names are bare action phrases** — no `<ROLE> -` prefix; no quoted strings.
- **Sub-step pattern** — `install` / `facts` / `configure` sub-files are kept only when each phase has genuine work; otherwise the role is a single `tasks/main.yml`.
