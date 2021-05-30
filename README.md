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

# Development Process

First, install conda. Then, create the `noteserver-dev` conda environment and
activate it using:

```
$ conda env create --force --file noteserver-dev.yml
$ conda activate noteserver-dev
```

Now, you'll want to create a new feature branch for your change. Do so with the
following:

```
# Create and checkout a new branch.
$ git checkout -b branch_name
# Upload that new branch to Github.
$ git push -u origin branch_name
```

Time to make your changes! Edit files in the `noteserver` directory and make
sure to add changes to `*_test.py` files for every `*.py` added or changed.
While coding, also make sure to use python's type-hint feature, as well as to
include docstrings for your functions and modules.

Now that your new change is looking good, run `./presubmit.sh` in order to
double check that everything is in order.

```
$ ./presubmit.sh
```

This script will run a linter, auto-formatter, type checker, and all of our unit
tests. If this script succeeds, you are now ready to start a pull request. If it
fails, check through the logs in order to determine what it would like you to
change.

Create a new commit on your branch and push your changes to Github:

```
$ git add .
$ git commit -m "My beautiful commit message."
$ git push
```

Now you can go to Github and [start a pull request](https://bit.ly/3omDiCT).


# Testing with VIM

So far, the easiest way to test Noteserver in a real editor is to use the
following snippet in your `.vimrc`


```
" Use the Plugged plugin managher to install vim-lsp. When you first boot vim,
" make sure to run `:PlugInstall`
call plug#begin('~/.vim/plugged')
Plug 'prabirshrestha/vim-lsp'
call plug#end()

" Configure vim to detect `.note` files as type `note`.
autocmd BufNewFile,BufRead *.note set ft=note

" Tell vim-lsp to start `noteserver` when we open a `note` file. To help debug
" problems, we will write noteserver logs to the `./noteserver.log` file.
au User lsp_setup call lsp#register_server({
     \ 'name': 'noteserver',
     \ 'cmd': {server_info->['python', '-m', 'noteserver',
     \                       '--log_path=./noteserver.log', '--verbose']},
     \ 'allowlist': ['note']
     \ })
```

You can now launch vim with noteserver using the following:

```
$ vim test.note
```
