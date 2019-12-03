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

# Geneate a summary table

The following command will generate a *csv* file with the summary of the participant groups.

```
python summary_csv.py
```

The resulting file is `summary.csv`.