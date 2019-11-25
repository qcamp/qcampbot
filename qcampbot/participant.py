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

from qcampbot.config import repo
from qcampbot.group import Group


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
