# -*- coding: utf-8 -*-
# Copyright (c) 2026 my-perfect-system contributors
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Identity filter plugins for the mps.base.identity resolve protocol.

Replaces the heavy Jinja2 data-shaping blocks that used to live in
`roles/identity/tasks/main.yml`. Each filter is a small, testable
function. The role's tasks are now a thin orchestrator that calls:

  - ``mps_resolve_users(users_list, users_catalog)`` — produces
    ``identity_users_resolved`` (a unified list combining ``users_list``
    entries with their matching ``users_catalog`` fields).
  - ``mps_user_groups(users)`` — produces a flat, deduplicated list of
    all group names referenced by each user's ``group`` and ``groups``
    fields.

The per-user role filter ``mps_filter_users`` is also defined here so
the entire identity/filter_plugins surface lives in one module.
"""

from __future__ import annotations


def _mps_filter_users(users, role_key=None, state="present"):
    if not users:
        return []
    filtered = [u for u in users if u]
    if state is not None:
        filtered = [u for u in filtered if u.get("state") == state]
    if role_key is not None:
        filtered = [u for u in filtered if u.get("user_roles", {}).get(role_key, False)]
    return filtered


def _mps_resolve_users(users_list, users_catalog):
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


def _mps_user_groups(users):
    if not users:
        return []
    names = []
    for u in users:
        if not u:
            continue
        if u.get("group"):
            names.append(u["group"])
        for g in u.get("groups") or []:
            names.append(g)
    seen = set()
    return [n for n in names if not (n in seen or seen.add(n))]


class FilterModule:
    def filters(self):
        return {
            "mps_filter_users": _mps_filter_users,
            "mps_resolve_users": _mps_resolve_users,
            "mps_user_groups": _mps_user_groups,
        }
