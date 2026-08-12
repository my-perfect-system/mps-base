# -*- coding: utf-8 -*-
# Copyright (c) 2026 my-perfect-system contributors
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Filter plugin: filter the per-user list by `user_roles` key and `state`.

Used by per-user roles (e.g. `mps.development.latex`) to iterate only the
users that have opted into the role-specific `user_roles.<key>` flag, while
excluding `absent` users and empty entries. Replaces the per-role
`when: - item.user_roles.<key> | default(false)` + `- item.state == 'present'`
+ `user != {}` boilerplate.

Usage::

    loop: "{{ identity_users_resolved | mps_filter_users('development_latex') }}"
    loop_control:
      label: "{{ item.name }}"
    vars:
      user: "{{ item }}"

If ``role_key`` is omitted the filter returns users filtered only by state
and emptiness (useful for roles that should run for every present user).
"""


def _mps_filter_users(users, role_key=None, state="present"):
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
        return {
            "mps_filter_users": _mps_filter_users,
        }
