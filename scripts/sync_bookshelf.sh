#!/bin/bash

# exit when any command fails
set -e;

# NOTE: Assume all requirements are already installed from post_create_command.sh in .devcontainer
# echo "Install virtualenv"
# pip3 install virtualenv;

# echo "Create venv-bookshelf-syncer"
# python3 -m venv ./venvs/venv-bookshelf-syncer;

# echo "Activate venv-bookshelf-syncer"
# source ./venvs/venv-bookshelf-syncer/bin/activate;

# echo "Install from ./src/bookshelf/syncer/requirements.txt"
# pip3 install -r ./src/bookshelf/syncer/requirements.txt;

echo "Running goodreads_translator.py"
python3 ./src/bookshelf/syncer/goodreads_translator.py --working-directory ./src/bookshelf/syncer;

echo "Building f3_syncer.ts"
tsc ./src/bookshelf/syncer/f3_syncer.ts;

echo "Running f3_syncer.js"
node ./src/bookshelf/syncer/f3_syncer.js;

# echo "Deactivate venv"
# deactivate;