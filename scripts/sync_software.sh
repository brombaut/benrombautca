#!/bin/bash

# exit when any command fails
set -e;

echo "Install virtualenv"
pip install virtualenv;

echo "Create venv-software-syncer"
python3 -m venv ./venvs/venv-software-syncer;

echo "Activate venv-software-syncer"
source ./venvs/venv-software-syncer/bin/activate;

echo "Install from ./src/bookshelf/syncer/requirements.txt"
pip install -r ./src/software/syncer/requirements.txt;

echo "Running goodreads_translator.py"
python3 ./src/software/syncer/readme_syncer.py --software-meta-file ./src/software/software_articles_meta.json --software-content-file ./src/software/software_articles_content.json;

echo "Deactivate venv"
deactivate;