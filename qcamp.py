from github import Github
import yaml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

gh = Github(config['token'])

repo = gh.get_repo("%s/%s" % (config['org'], config['repo']))
user = gh.get_user()


def somebody_mentions_me(comment):
    return '@qcamp' in comment.body


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
    def allow_participants(self):
        return self.issue.state != 'open' or len(self.issue.assignees) < 5

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


class JoinRequest:
    def __init__(self, git_comment):
        self.group = Group(number=int(git_comment.issue_url.rsplit('/', 1)[-1]))
        self.participant = Participant(handler=git_comment.user.login)
        self._issue = None
        self._git_comment = git_comment

    def do(self):
        if not self.group.allow_participants:
            self.report_group_full()
            return
        if self.participant.groups is not None:
            self.report_participant_in_other_group()
            return
        self.group.add_participant(self.participant)
        self.report_participant_added()

    def report_participant_added(self):
        self._git_comment.create_reaction('+1')
        print('User @%s added to #%s' % (self.participant.handler, self.group.number))

    def report_participant_in_other_group(self):
        self._git_comment.create_reaction('confused')
        print('User @%s is already in #%s so they cannot be added to #%s' % (
            self.participant.handler, self.participant.groups[0].number, self.group.number))

    def report_group_full(self):
        self._git_comment.create_reaction('-1')
        print('User @%s could not be added to #%s (group full)' % (self.participant.handler,
                                                                  self.group.number))


for comment in repo.get_issues_comments():
    if somebody_mentions_me(comment):
        join_request = JoinRequest(comment)
        join_request.do()
