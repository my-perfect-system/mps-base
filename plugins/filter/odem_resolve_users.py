# -*- coding: utf-8 -*-
# Copyright (c) 2026 my-perfect-system contributors
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""odem_resolve_users — resolve users_list against users_catalog for odem.base.identity."""

from __future__ import annotations

DOCUMENTATION = r"""
name: odem_resolve_users
short_description: Resolve users_list entries against users_catalog
version_added: 0.3.0
author: my-perfect-system contributors
description:
  - Combines the raw C(users_list) assignment list with the matching
    C(users_catalog) entries to produce the unified C(identity_users_resolved)
    structure consumed by the odem.* per-user roles.
  - For each C(users_list) entry, the matching C(users_catalog) entry is
    looked up by its C(name) (the catalog key). The catalog entry's fields are
    preserved, and C(id), C(name), C(state) and C(user_roles) are overlaid.
  - C(name) (the OS username) defaults to the catalog entry's C(name) field,
    falling back to the catalog key (the unique id) when absent.
  - C(state) is taken from the C(users_list) entry (defaulting to C(present)).
  - C(user_roles) is taken from the catalog entry (defaulting to an empty dict).
positional: users_catalog
options:
  _input:
    description: The C(users_list) assignment list.
    type: list
    elements: dict
    required: true
  users_catalog:
    description:
      - The C(users_catalog) mapping keyed by unique id.
      - Each entry supplies the identity fields for the matching C(users_list) item.
    type: dict
    required: true
"""

EXAMPLES = r"""
- name: Resolve users into the identity_users_resolved fact
  ansible.builtin.set_fact:
    identity_users_resolved: "{{ users_list | odem.base.odem_resolve_users(users_catalog) }}"
"""

RETURN = r"""
_value:
  description:
    - A list of dicts, one per C(users_list) entry, with all catalog fields
      preserved plus C(id), C(name), C(state) and C(user_roles).
  type: list
  elements: dict
"""


def odem_resolve_users(users_list, users_catalog):
    if not users_list:
        return []
    catalog = users_catalog or {}
    resolved = []
    for entry in users_list:
        if not entry or "name" not in entry:
            continue
        catalog_entry = catalog.get(entry["name"]) or {}
        merged = dict(catalog_entry)
        merged["id"] = entry["name"]
        merged["name"] = catalog_entry.get("name", entry["name"])
        merged["state"] = entry.get("state", "present")
        merged["user_roles"] = catalog_entry.get("user_roles", {}) or {}
        resolved.append(merged)
    return resolved


class FilterModule:
    def filters(self):
        return {"odem_resolve_users": odem_resolve_users}
