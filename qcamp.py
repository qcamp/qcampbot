from github import Github
import yaml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

gh = Github(config['token'])

repo = gh.get_repo("%s/%s" % (config['org'], config['repo']))
user = gh.get_user()


def somebody_mentions_me(comment):
    return '@qcamp' in comment.body


def add_to_group_if_possible(comment):
    issue_no = int(comment.issue_url.rsplit('/', 1)[-1])
    issue = repo.get_issue(issue_no)
    if issue.state == 'open' == len(issue.assignees) >= 5 :
        print('User %s could not be added to %s (group full)' % (comment.user, issue_no))
        return
    issue.add_to_assignees(comment.user)
    print('User %s added to %s' % (comment.user, issue_no))


for comment in repo.get_issues_comments():
    if somebody_mentions_me(comment):
        add_to_group_if_possible(comment)
