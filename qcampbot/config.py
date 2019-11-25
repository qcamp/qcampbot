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

from github import Github
from termcolor import colored
import yaml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

gh = Github(config['token'])

repo = gh.get_repo("%s/%s" % (config['org'], config['repo']))
user = gh.get_user()
team_limit = config['team limit']


def somebody_mentions_me(comment):
    return user.login in comment.body


class Participant:
    def __init__(self, handler=None):
        self.handler = handler
        self._groups = None

    @property
    def groups(self):
        if self._groups is None:
            self._groups = [Group(issue=issue) for issue in repo.get_issues(state='open',
                                                                            assignee=self.handler)]
        return self._groups


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


def highlight(text):
    return colored(text, attrs=['bold'])


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
        print(self.reactions[reaction], end=' - ')
        print(to_print)


def get_join_requests(repo):
    for comment in repo.get_issues_comments():
        if somebody_mentions_me(comment):
            yield JoinRequest(comment)
