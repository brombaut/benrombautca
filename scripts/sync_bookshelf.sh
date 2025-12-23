#!/bin/bash

# exit when any command fails
set -e;

echo "Install virtualenv"
pip3 install virtualenv;

echo "Create venv-bookshelf-syncer"
python3 -m venv ./venvs/venv-bookshelf-syncer;

echo "Activate venv-bookshelf-syncer"
source ./venvs/venv-bookshelf-syncer/bin/activate;

echo "Install from ./src/bookshelf/syncer/requirements.txt"
pip3 install -r src/bookshelf/syncer_v2/requirements.txt;

echo "Running 00_goodreads_scraper.py"
python3 src/bookshelf/syncer_v2/00_goodreads_scraper.py --working-directory ./src/bookshelf/syncer_v2;

echo "Running 02_all_books_flattener.py"
python3 src/bookshelf/syncer_v2/02_all_books_flattener.py --working-directory ./src/bookshelf/syncer_v2;

echo "Converting images to webp"
pip3 install Pillow;
python3 scripts/convert_images_to_webp.py src/bookshelf/syncer_v2/book_thumbnails_v2;

echo "Deleting non-webp images"
python3 scripts/delete_non_webp_images.py src/bookshelf/syncer_v2/book_thumbnails_v2;

echo "Running 03_show_missing_thumbnails.py"
python3 src/bookshelf/syncer_v2/03_show_missing_thumbnails.py --working-directory ./src/bookshelf/syncer_v2;


echo "Deactivate venv"
deactivate;