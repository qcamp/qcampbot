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
import yaml
import csv

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

if config.get('base_url', None):
    gh = Github(config['token'], base_url=config['base_url'])
else:
    gh = Github(config['token'])

repo = gh.get_repo("%s/%s" % (config['org'], config['repo']))
organization = gh.get_organization(config['org'])

if config.get('base_url', None):
    coaches_team = None
else:
    coaches_team = organization.get_team_by_slug(config['coaches team'])

user = gh.get_user()
team_limit = config['team limit']
exclude_issues = config['exclude issues']
rate_config = config['rate']
summary = config['csv files']['summary']
handlers = config['csv files']['handlers']

user_handlers = {}
try:
    with open(handlers) as csvfile:
        user_handlers = {row[0]: row[1] for row in csv.reader(csvfile)}
except FileNotFoundError:
    print(f'no {handlers} file')
except IndexError:
    print(f'file {handlers} out of format')
