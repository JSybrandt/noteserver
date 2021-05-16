#!/bin/bash


# Checking that everything is in its right place:

error(){
  # Reports and error and exits.
  MSG=$1
  echo "Presubmit failed. $MSG"
  exit 1
}

phase(){
  # Delineates between presubmit phases.
  NAME=$1
  echo
  echo
  echo "--- $NAME ---"
}

if [[ ! -d "./noteserver" ]]; then
  error "Must run in project root."
fi

if ! which pylint; then
  error "Failed to find pylint."
fi

if ! which yapf; then
  error "Failed to find yapf."
fi

if ! which pytype; then
  error "Failed to find pytype."
fi

PACKAGE_DIR="./noteserver"

phase "linting"
# Exits nonzero if code quality score is less than `fail-under`.
pylint --jobs=0 --fail-under=10 --indent-string="  " \
  --load-plugins="pylint.extensions.docparams" $PACKAGE_DIR
if [[ $? -ne 0 ]]; then
  error "Linter errors."
fi

phase "formatting"
yapf --verbose --in-place --parallel --recursive \
  --style='{based_on_style: google indent_width: 2}' \
  "$PACKAGE_DIR"
if [[ $? -ne 0 ]]; then
  error "Formatter error."
fi

phase "type checking"
pytype -V 3.8 --check-parameter-types --jobs=auto --keep-going $PACKAGE_DIR
if [[ $? -ne 0 ]]; then
  error "Type checking error."
fi

phase "testing"
python -m unittest discover --pattern="*_test.py" --verbose
if [[ $? -ne 0 ]]; then
  error "Unit tests failed."
fi

phase "Success!"
