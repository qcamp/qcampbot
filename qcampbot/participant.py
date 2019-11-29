# -*- coding: utf-8 -*-

# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from .config import repo, coaches_team
from .group import Group


class Participant:
    def __init__(self, handler=None, named_user=None):
        self.handler = None
        self._groups = None
        self._named_user = None

        if handler is not None:  # string github handler
            self.handler = handler
        if named_user is not None:  # github.NamedUser.NamedUser
            self._named_user = named_user
            self.handler = named_user.login

    @property
    def groups(self):
        if self._groups is None:
            self._groups = [Group(issue=issue) for issue in repo.get_issues(state='open',
                                                                            assignee=self.handler)]
        return self._groups

    @property
    def is_coach(self):
        return coaches_team.has_in_members(self._named_user)
