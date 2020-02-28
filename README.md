# qCampBot (@qcamp)

`@qcamp` user should have admin privilege in the event repo.


# Requirements and configuration

Requires Python 3.7 or higher and the modules in `requirements.txt`.

The configuration file is also require as `config.yaml`. An example of the configuration file can be found in `config-example.yaml`.

# Team formation
During team formation, the script `team_formation.py` should be running.

```
python team_formation.py
```

It performs two operations in a loop until `ctrl-C`: tags the team that are full as `group is full` (and removes the tag if, for some reason, members are removed) and assign members to a team when a participant mentions `@qcamp`.

## Internal hackathons
When the hackathon is internal, participants assign themselves to groups, so they need monitoring. For that, the script `team_formation_internal.py` should be running during team formation.

```
python team_formation_internal.py
```

This script does not monitor `@qcamp` (this user does not exist internally) but does the same team tagging as `team_formation.py`. Additional, checks that members are in a single team.

Internal hackathons do not have the notion of coaches.

# Generate a summary table

The following command will generate a *csv* file with the summary of the participant groups.

```
python summary_csv.py
```

The resulting file is `summary.csv`.

# Add participants full name

The file `handler_fullname.csv` allows to relate a GitHub handler with a participant full name. The format is:

```
<GitHub handler>,<Full name>
```

If the file is not present (or the participant is not in the file), the script will try to get the full name from the GitHub profile.

# Checklist to deploy a hackathon repo

 - Create a repo from the template: https://github.com/qiskit-community/qiskit-camp-template -> `Use this template`.
 - Edit the `description` and the `website`.
 - In settings add `qbotcamp` as Admin and `qiskit-community/Coaches` with Triage privileges.
 - In settings, remove `wiki` and `projects`.
 - Set issue labels as in template.
 - Edit README file where ⚠️.