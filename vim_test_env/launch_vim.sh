#!/bin/bash

# Get the location of this script, which should live in
# .../noteserver/vim_test_env.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
VIMRC="$SCRIPT_DIR/vimrc"
VIM_LSP_PLUG_DIR="$SCRIPT_DIR/bundle/vim_lsp"

# Vim runtimepath is comma-separated.
RUNTIME_PATH="$VIMRC,$VIM_LSP_PLUG_DIR"

vim -c "set rtp=$RUNTIME_PATH" -u "$VIMRC"
