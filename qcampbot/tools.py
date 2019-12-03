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

import time
from datetime import datetime
from termcolor import colored

from .config import gh, rate_config


def highlight(text):
    return colored(text, attrs=['bold'])


def print_log(to_print, icon=None):
    print(f'[ {time.strftime("%H:%M:%S", time.localtime())} ] {icon}  {to_print}')


def check_rate_limit(previous_remaining=None, previous_reset=None):
    core_rate = gh.get_rate_limit().core
    remaining = core_rate.remaining
    reset = int(gh.get_rate_limit().core.reset.timestamp() - datetime.utcnow().timestamp())
    rate_limit = rate_config['limit']
    sleep = rate_config['sleep']
    if previous_remaining is None or previous_reset is None:
        return remaining, reset
    rate = (previous_remaining-remaining)/(previous_reset-reset)
    if rate > rate_limit:
        print_log(f'Looping too fast ({rate:.2f} req/sec!). Sleep({sleep})', icon='\N{STOPWATCH}')
        time.sleep(sleep)
    print_log(f'There are {remaining} reqs in the coming {reset} secs.', '\N{Construction Sign}')
    return remaining, reset
