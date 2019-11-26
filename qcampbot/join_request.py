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

from .config import user
from .participant import Participant
from .group import Group
from .tools import highlight, print_log


class JoinRequest:
    reactions = {'+1': u'👍',
                 '-1': u'👎',
                 'confused': u'😕'}

    def __init__(self, git_comment):
        self.group = Group(number=int(git_comment.issue_url.rsplit('/', 1)[-1]))
        self.participant = Participant(handler=git_comment.user.login)
        self._git_comment = git_comment

    def do(self):
        if self.group.closed:
            self.report_group_closed()
            return
        if self.group.full:
            self.report_group_full()
            return
        if self.participant.groups is not None:
            self.report_participant_in_other_group()
            return
        self.group.add_participant(self.participant)
        self.report_participant_added()

    def report_participant_added(self):
        handler = highlight('@%s' % self.participant.handler)
        want_to = highlight('#%s' % self.group.number)
        stdout = f'User {handler} added to {want_to}.'
        self.report('+1', stdout)

    def report_participant_in_other_group(self):
        current = highlight('#%s' % self.participant.groups[0].number)
        want_to = highlight('#%s' % self.group.number)
        handler = highlight('@%s' % self.participant.handler)
        comment = None
        if current == self.group.number:
            stdout = (f'User {self.participant.handler} is already in {self.group.number}.'
                      f'so nothing to do')
        else:
            stdout = (f'User {handler} is already in {current} so they cannot '
                      f'be added to {want_to}')
            current = self.participant.groups[0].number
            comment = (
                f'Hi @{self.participant.handler}! I could not add you to this group because you '
                f'are already in #{current}. If you want to change teams, unassign yourself from '
                f'#{current} and write me again here.')
        self.report('confused', stdout, comment)

    def report_group_full(self):
        handler = highlight('@%s' % self.participant.handler)
        group = highlight('#%s' % self.group.number)
        stdout = f'User {handler} could not be added to {group} (group full).'
        comment = (f'Hi @{self.participant.handler}! I could not add you to this group '
                   f'because it is full.')
        self.report('-1', stdout, comment)

    def report_group_closed(self):
        handler = highlight('@%s' % self.participant.handler)
        group = highlight('#%s' % self.group.number)
        stdout = f'User {handler} could not be added to {group} (group closed).'
        comment = (f'Hi @{self.participant.handler}! I could not add you to this group '
                   f'because it is closed.')
        self.report('-1', stdout, comment)

    def report(self, reaction, to_print, comment=None):
        self._git_comment.create_reaction(reaction)
        if comment:
            self.group.issue.create_comment(comment)
        print_log(to_print, self.reactions[reaction])


def somebody_mentions_me(comment):
    return ("@%s" % user.login) in comment.body


def still_pending(comment):
    return user.login not in [ i.user.login for i in comment.get_reactions()]


def get_join_requests(repo):
    for comment in repo.get_issues_comments():
        if somebody_mentions_me(comment) and still_pending(comment):
            yield JoinRequest(comment)
