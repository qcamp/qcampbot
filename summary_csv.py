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

import csv
from qcampbot import repo, get_groups


with open('summary.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(['Title', '#', 'Coach', 'Members'])
    for group in get_groups(repo).values():
        spamwriter.writerow([group.title,
                             group.number,
                             ', '.join([coach.full_name for coach in group.coaches]),
                             ', '.join([participant.full_name for participant in
                                        group.participants])])
