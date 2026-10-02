#!/bin/bash

# exit when any command fails
set -e;

echo "Install virtualenv"
pip3 install virtualenv;

echo "Create venv-articles-syncer"
# Recreate from scratch: pypandoc and pypandoc_binary ship the same module, so a
# leftover unpinned pypandoc in a reused venv would clash with the pin (#548).
rm -rf ./venvs/venv-articles-syncer;
python3 -m venv ./venvs/venv-articles-syncer;

echo "Activate venv-articles-syncer"
source ./venvs/venv-articles-syncer/bin/activate;

echo "Install from src/blog/content/requirements.txt"
pip3 install -r src/blog/content/requirements.txt;

echo "Running python3 src/blog/content/01_md_to_html_converter.py;"
python3 src/blog/content/01_md_to_html_converter.py;

echo "Running python3 src/blog/content/02_existing_html_articles_syncer.py;"
python3 src/blog/content/02_existing_html_articles_syncer.py;


echo "Deactivate venv"
deactivate;