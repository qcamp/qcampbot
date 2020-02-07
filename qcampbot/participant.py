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

from .config import repo, gh, coaches_team, user_handlers
from .group import Group
from .tools import print_log


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
        if coaches_team is None:
            return False
        return coaches_team.has_in_members(self._named_user)

    @property
    def named_user(self):
        if self._named_user is None:
            self._named_user = gh.get_user(self.handler)
        return self._named_user

    @property
    def full_name(self):
        name = user_handlers.get(self.handler)
        if name is None:
            name = self.named_user.name
        if name is None:
            print_log(f'The handler {self.handler} does not have a name', icon='\N{CROSS MARK}')
            name = f"({self.handler})"
        return name

    def check_group_membership(self, max_amount=1):
        """
        Checks that the member has a relation with the group or groups
        :param max_amount: maximum amount of groups that the participant can participate in
        :return:
        """
        self._groups = None
        if len(self.groups) > max_amount:
            str_groups = ", ".join([f"#{group.number}" for group in self.groups])
            print_log(
                f'{self.full_name} ({self.handler}) is in more than one team: {str_groups}',
                icon='\N{CROSS MARK}')

    def __eq__(self, other):
        return self.handler == other.handler

    def __hash__(self):
        return hash(self.handler)

def get_participants(repo):
    participants = {Participant(named_user=assignee) for assignee in repo.get_assignees()}
    return participants
