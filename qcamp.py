from github import Github
import yaml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

gh = Github(config['token'])

repo = gh.get_repo("%s/%s" % (config['org'], config['repo']) )
user = gh.get_user()

for notification in user.get_notifications(all=True):
    print(notification)
