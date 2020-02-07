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

from .config import repo, team_limit, exclude_issues
from .tools import print_log


class Group:
    def __init__(self, issue=None, number=None):
        self._number = None
        self._issue = None
        self._participants = []
        self._coaches = []
        if issue:
            # github.Issue
            self._number = issue.number
            self._issue = issue
        if number:
            # int: Issue number
            self._number = number

    def add_participant(self, participant):
        self.issue.add_to_assignees(participant.handler)

    @property
    def full(self):
        return len(self.participants) >= team_limit

    def mark_as(self, label, message):
        if label not in [i.name for i in self.issue.labels]:
            self.issue.add_to_labels(label)
            print_log(message, icon='\N{LABEL}')

    def mark_as_not(self, label, message):
        if label in [i.name for i in self.issue.labels]:
            self.issue.remove_from_labels(label)
            print_log(message, icon='\N{LABEL}')

    def mark_as_full(self):
        self.mark_as('group is full', f'Label "full" added to the group {self.number}.')

    def mark_as_not_full(self):
        self.mark_as_not('group is full', f'Label "full" removed to the group {self.number}.')

    @property
    def closed(self):
        return self.issue.state != 'open'

    @property
    def participants(self):
        if not len(self._participants):
            from .participant import Participant
            for assignee in self.issue.assignees:
                participant = Participant(named_user=assignee)
                if not participant.is_coach:
                    self._participants.append(participant)
        return self._participants

    @property
    def coaches(self):
        if not len(self._coaches):
            from .participant import Participant
            for assignee in self.issue.assignees:
                participant = Participant(named_user=assignee)
                if participant.is_coach:
                    self._coaches.append(participant)
        return self._coaches

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

    @property
    def title(self):
        return self.issue.title

    def update_full_tag(self):
        self.update()
        if self.full:
            self.mark_as_full()
        else:
            self.mark_as_not_full()

    def update_toomany_tag(self):
        if len(self.participants) > team_limit:
            self.mark_as_toomany()
        else:
            self.mark_as_not_toomany()

    def update(self):
        if self._issue:
            self._issue.update()

    def mark_as_toomany(self):
        self.mark_as('too many members!',
                     f'Label "too many members" added to the group {self.number}.')

    def mark_as_not_toomany(self):
        self.mark_as_not('too many members!',
                         f'Label "too many members" removed to the group {self.number}.')


group_cache = {issue.number: Group(issue=issue) for issue in repo.get_issues(state='open')}


def get_groups(repo):
    groups = {issue.number: Group(issue=issue) for issue in repo.get_issues(state='open')}
    groups.update(group_cache)
    for to_exclude in exclude_issues:
        groups.pop(to_exclude, None)
    return groups
