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

from qcampbot.config import repo, team_limit


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
        if len(self.issue.assignees) >= team_limit:
            self.mark_as_full()
            return True
        else:
            self.mark_as_not_full()
            return False

    def mark_as_full(self):
        self.issue.add_to_labels('group is full')

    def mark_as_not_full(self):
        if 'group is full' in [i.name for i in self.issue.labels]:
            self.issue.remove_from_labels('group is full')

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
