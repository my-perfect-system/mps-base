# -*- coding: utf-8 -*-
# Copyright (c) 2026 my-perfect-system contributors
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""odem_user_groups — flatten per-user group names for odem.base.identity."""

from __future__ import annotations

DOCUMENTATION = r"""
name: odem_user_groups
short_description: Flatten group names referenced by resolved users
version_added: 0.3.0
author: my-perfect-system contributors
description:
  - Produces a flat, deduplicated list of all group names referenced by each
    user's C(group) (primary) and C(groups) (supplementary) fields.
  - Intended to run over the present subset of C(identity_users_resolved) to
    build the C(identity_user_groups) fact for C(odem.users.groups).
positional: _input
options:
  _input:
    description:
      - A list of resolved user dicts (typically
        C(identity_users_present)).
      - Each entry's C(group) and C(groups) fields, when set, contribute to
        the output.
    type: list
    elements: dict
    required: true
"""

EXAMPLES = r"""
- name: Extract the flat list of group names from present users
  ansible.builtin.set_fact:
    identity_user_groups: "{{ identity_users_present | odem.base.odem_user_groups }}"
"""

RETURN = r"""
_value:
  description: A flat, deduplicated list of group names.
  type: list
  elements: str
"""


def odem_user_groups(users):
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
        return {"odem_user_groups": odem_user_groups}
