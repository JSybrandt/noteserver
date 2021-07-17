#!/bin/bash

# Get the location of this script, which should live in
# .../noteserver/vim_test_env.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

VIMRC=$SCRIPT_DIR/vimrc

echo "Launching vim using $SCRIPT_DIR as the runtimepath."

vim --cmd "set rtp=$SCRIPT_DIR" -u "$VIMRC"
