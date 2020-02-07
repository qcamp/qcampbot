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

from qcampbot import repo, get_groups

try:
    while True:
        for group in get_groups(repo).values():
            group.update_full_tag()
            group.update_toomany_tag()

except KeyboardInterrupt:
    pass