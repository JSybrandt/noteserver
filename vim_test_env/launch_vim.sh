#!/bin/bash

# Get the location of this script, which should live in
# .../noteserver/vim_test_env.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

RUNTIME_PATH="$SCRIPT_DIR"
RUNTIME_PATH="$RUNTIME_PATH,$SCRIPT_DIR/vimrc"

# Go to the script dir so that all of the vimrc's file paths can be relative to
# the install directory.
cd $SCRIPT_DIR


 vim -c "set rtp=$RUNTIME_PATH" -u "$SCRIPT_DIR/vimrc" "$@"
