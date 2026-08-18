# `odem.base` Ansible Collection

Anchor collection for the `odem.*` ecosystem. Hosts shared conventions,
the per-user identity data model, and shared helpers. All leaf
collections depend on this.

## Galaxy metadata

- **namespace**: `odem`
- **name**: `base`
- **version**: `0.3.1`

See [`galaxy.yml`](galaxy.yml) for the canonical values.

## Roles

| Role | Description |
|---|---|
| [`odem.base.identity`](roles/identity/README.md) | Shared per-user identity model. Produces the `identity_users_*` facts every per-user role depends on. |
| [`odem.base.assert_debian13`](roles/assert_debian13/README.md) | Fail-fast assertion that target host runs Debian 13 (trixie). Used as a meta dependency by every role that requires Debian 13. |

## Filter plugins

| Filter | Purpose |
|---|---|
| `odem_filter_users(users, role_key, state='present')` | Filter `identity_users_resolved` by a `user_roles.<key>` flag — used by every per-user leaf role. |
| `odem_resolve_users(users_list, users_catalog)` | Resolve raw `users_list` entries against `users_catalog` to produce `identity_users_resolved`. |
| `odem_user_groups(users)` | Flat deduplicated list of group names referenced by `group` + `groups` fields. |

## Installation

```bash
ansible-galaxy collection install odem.base
```

Or build + install from source:

```bash
ansible-galaxy collection build
ansible-galaxy collection install odem-base-*.tar.gz
```

## Usage

`odem.base.identity` is a dependency — it is not invoked directly. To use it, declare it in your role's `meta/main.yml`:

```yaml
dependencies:
  - role: odem.base.identity
```

Then in your role tasks, iterate the resolved users:

```yaml
- name: Do per-user thing
  ansible.builtin.command: ...
  loop: "{{ identity_users_resolved | odem.base.odem_filter_users('your_role_key') }}"
  loop_control:
    label: "{{ item.name }}"
```

## Documentation

- [`AGENTS.md`](AGENTS.md) — developer-facing collection conventions
- Per-role documentation lives in each role's `README.md` (auto-generated)
- The cross-collection conventions (task naming, toggle variables, user-role denylist) are documented in the top-level `manage/AGENTS.md`

## License

GPL-3.0-or-later
