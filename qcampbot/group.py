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

from .config import repo, team_limit
from .tools import print_log


class Group:
    def __init__(self, issue=None, number=None):
        self._number = None
        self._issue = None
        if issue:
            # github.Issue
            self._number = issue.number
            self._issue = issue
        if number:
            # int: Issue number
            self._number = number

    def add_participant(self, participant):
        self.issue.add_to_assignees(participant.handler)
        self._issue = None

    @property
    def full(self):
        return len(self.issue.assignees) >= team_limit

    def mark_as_full(self):
        if 'group is full' not in [i.name for i in self.issue.labels]:
            self.issue.add_to_labels('group is full')
            print_log(f'Label "full" added to the group {self.number}.', icon=u'🏷')

    def mark_as_not_full(self):
        if 'group is full' in [i.name for i in self.issue.labels]:
            self.issue.remove_from_labels('group is full')
            print_log(f'Label "full" removed to the group {self.number}.', icon=u'🏷')

    @property
    def closed(self):
        return self.issue.state != 'open'

    @property
    def issue(self):
        if self._issue is None:
            self._issue = repo.get_issue(self.number)
        return self._issue

    @property
    def number(self):
        if self._number is None:
            self._number = self.issue.number
        return self._number

    def update_full_tag(self):
        if self.full:
            self.mark_as_full()
        else:
            self.mark_as_not_full()


def get_groups(repo):
    return [Group(issue=issue) for issue in repo.get_issues(state='open')]
