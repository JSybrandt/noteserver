# Noteserver
A cross platform backend for personal wikis.

# Docs

High-level spec: https://bit.ly/3eQnJQU

# Development Environment

Its recommended to use Conda to manage the python environment while developing
Noteserver.

Init or refresh your instance of the dev conda environment
(do this once to get started, or whenever someone else updates the dev
environment):

```
$ conda env create --force --file noteserver-dev.yml
```

Update the dev conda environment
(do this if you install anything in the dev environment):

```
$ conda env export -n noteserver-dev > noteserver-dev.yml
```

Activate the environment:
(do this before starting dev work):

```
$ conda activate noteserver-dev
```
