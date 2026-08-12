---
namespace: odem
collection: base
role: identity
---

# `odem.base.identity`

Shared identity model for the odem.* ecosystem

## Default variables

| Variable | Default | Description |
|---|---|---|
| `admin_groups` | `- admin<br>- config` |  |
| `user_append_groups` | `true` |  |
| `user_create_home` | `true` |  |
| `user_expires` | `-1` |  |
| `user_groups` | `[]` |  |
| `user_password` | `changeme` |  |
| `user_roles_default` | `{ terminal_bash: …, terminal_vim: …, terminal_nvim: … }` |  |
| `user_roles_minimal` | `{ terminal_bash: …, terminal_vim: … }` |  |
| `user_shell` | `/bin/bash` |  |
| `user_system` | `false` |  |
| `users_catalog` | `{  }` | Identity catalog keyed by a free-form unique id. Keys are NOT validated against a fixed set; they are only used to reference entries from users_list. The real OS username is taken from each entry's name field. If name is omitted, it defaults to the catalog key (the unique id). Each value is a dict describing a single user entity. The supported schema is documented under the options block below. |
| `users_list` | `[]` | Assignment list. Each entry references a users_catalog key via name and sets state. No other fields are read from users_list entries; all identity comes from the catalog. |

## Dependencies

None.

## Example usage

```yaml
- hosts: all
  roles:
    - odem.base.identity
```

## Role metadata

- **Min Ansible version**: `2.16.0`
- **License**: GPL-3.0-or-later
- **Platforms**: Debian (trixie)
- **Tasks file lines**: 51

## Related files

- [`meta/main.yml`](meta/main.yml) — galaxy_info + role dependencies
- [`meta/argument_specs.yml`](meta/argument_specs.yml) — variable spec (the source of the variable table above)
- [`defaults/main.yml`](defaults/main.yml) — variable defaults (the source of the default values above)