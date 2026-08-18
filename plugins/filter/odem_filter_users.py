# -*- coding: utf-8 -*-
# Copyright (c) 2026 my-perfect-system contributors
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""odem_filter_users — per-user role opt-in filter for the odem.base.identity model."""

from __future__ import annotations

DOCUMENTATION = r"""
name: odem_filter_users
short_description: Filter resolved users by a user_roles opt-in flag
version_added: 0.3.0
author: my-perfect-system contributors
description:
  - Filters the list produced by C(odem.base.odem_resolve_users) (typically
    stored in the C(identity_users_resolved) fact) to present users that opted
    into a specific C(user_roles) key.
  - Used by per-user roles to loop only over users that enabled a given role
    (for example C(terminal_bash), C(development_opencode)).
  - Empty or falsy entries in the input list are skipped internally.
positional: role_key
options:
  _input:
    description: A list of resolved user dicts, typically C(identity_users_resolved).
    type: list
    elements: dict
    required: true
  role_key:
    description:
      - The C(user_roles) key to filter on (for example C(terminal_bash)).
      - When omitted, no role filtering is applied.
    type: str
    required: false
  state:
    description:
      - Only keep users whose C(state) matches this value.
      - Set to C(null) to disable state filtering and keep all users.
    type: str
    default: present
    choices: [present, absent]
"""

EXAMPLES = r"""
- name: Configure bash only for users that opted into terminal_bash
  ansible.builtin.debug:
    msg: "configuring bash for {{ entity.name }}"
  loop: "{{ identity_users_resolved | odem.base.odem_filter_users('terminal_bash') }}"
  loop_control:
    loop_var: entity
"""

RETURN = r"""
_value:
  description: A list of user dicts matching the requested role key and state.
  type: list
  elements: dict
"""


def odem_filter_users(users, role_key=None, state="present"):
    if not users:
        return []
    filtered = [u for u in users if u]
    if state is not None:
        filtered = [u for u in filtered if u.get("state") == state]
    if role_key is not None:
        filtered = [u for u in filtered if u.get("user_roles", {}).get(role_key, False)]
    return filtered


class FilterModule:
    def filters(self):
        return {"odem_filter_users": odem_filter_users}
