import datetime
import requests
import json
import os
import logging
import pypandoc

from argparse import ArgumentParser
from pypandoc.pandoc_download import download_pandoc

logging.basicConfig(
    format='%(asctime)s :: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG
)

parser = ArgumentParser()
parser.add_argument(
    "-smf",
    "--software-meta-file",
    dest="software_meta_file",
    required=True,
)
parser.add_argument(
    "-scf",
    "--software-content-file",
    dest="software_content_file",
    required=True,
)
args = parser.parse_args()

SOFTWARES = [
    {
        "id": "benrombautca",
        "url": "https://raw.githubusercontent.com/brombaut/benrombautca/main/README.md"
    },
    {
        "id": "firebase_firestore_facade",
        "url": "https://raw.githubusercontent.com/brombaut/firebase-firestore-facade/main/README.md",
    },
    {
        "id": "game_of_life",
        "url": "https://raw.githubusercontent.com/brombaut/game-of-life/main/README.md"
    },
    {
        "id": "article_scraper",
        "url": "https://raw.githubusercontent.com/brombaut/article-scraper/main/README.md",
    }
]


def run():
    try:
        download_pandoc()
    except Exception as e:
        logging.error("")
        raise e
    logging.info("Parsing args...")
    meta_file_path = args.software_meta_file
    logging.info(f"meta_file_path={meta_file_path}")
    content_file_path = args.software_content_file
    logging.info(f"content_file_path={content_file_path}")
    logging.info("Reading existing Software Articles...")
    existing_sas = build_existing_sas(meta_file_path, content_file_path)
    logging.info("Getting fresh Software Articles...")
    fresh_sas = build_fresh_sas(SOFTWARES)
    logging.info("Syncing the two...")
    updated = update_existing_with_fresh(existing_sas, fresh_sas)
    logging.info("Writing synced data to files...")
    write_updated_to_files(updated, meta_file_path, content_file_path)
    logging.info("Done")


def build_existing_sas(meta_file_path, content_file_path):
    metas = load_json_file(meta_file_path)
    contents = load_json_file(content_file_path)
    sas = dict()
    for m in metas:
        sas[m['_id']] = m
        for c in contents:
            if c['_id'] == m['_id']:
                sas[m['_id']]['_body'] = c['_body']
    return sas


def build_fresh_sas(sws):
    sas = dict()
    for s in sws:
        markdown_read_me = get_readme_text(s['url'])
        html_readme = convert_markdown_to_html(markdown_read_me)
        sas[s['id']] = {
            "_id": s['id'],
            "_body": html_readme
        }
    return sas


def update_existing_with_fresh(existing_sas, fresh_sas):
    for _, fsa in fresh_sas.items():
        if fsa['_id'] not in existing_sas:
            logging.info(f"New software article: {fsa['_id']}")
            existing_sas[fsa['_id']] = {
                "_id": fsa['_id'],
                "_title": "",
                "_createdAt": datetime.datetime.now(),
                "_updatedAt": datetime.datetime.now(),
                "_description": "",
                "_show": False,
                "_externalRepos": list(),
                "_techUsed": list(),
                "_body": fsa['_body'],
            }
        else:
            logging.info(f"Existing software article: {fsa['_id']}")
            existing_sa = existing_sas[fsa['_id']]
            if existing_sa['_body'] != fsa['_body']:
                logging.info(f"\tNeeds updating")
                # update existing sa
                existing_sa['_body'] = fsa['_body']
                existing_sa['_updatedAt'] = datetime.datetime.now()
            else:
                logging.info(f"\tDoes not need updating")
    return existing_sas


def write_updated_to_files(updated, meta_file_path, content_file_path):
    metas = list()
    contents = list()
    for _, u in updated.items():
        metas.append({
            "_id": u['_id'],
            "_title": u['_title'],
            "_createdAt": u['_createdAt'],
            "_updatedAt": u['_updatedAt'],
            "_description": u['_description'],
            "_show": u['_show'],
            "_externalRepos": u['_externalRepos'],
            "_techUsed": u['_techUsed'],
        })
        contents.append({
            "_id": u['_id'],
            "_body": u['_body'],
        })
    write_json_file(meta_file_path, metas)
    write_json_file(content_file_path, contents)


############################
# Util Functions
############################
def load_json_file(file_path):
    with open(file_path) as f:
        return json.load(f)


def write_json_file(file_path, contents):
    with open(file_path, 'w') as f:
        json.dump(contents, f, default=str, indent=2)


def get_readme_text(url):
    response = requests.get(url)
    return response.text


def convert_markdown_to_html(markdown):
    result = pypandoc.convert_text(markdown, 'html', format='md')
    return result


if __name__ == "__main__":
    run()
