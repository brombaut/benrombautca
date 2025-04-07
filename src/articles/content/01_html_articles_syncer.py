import json
import os
import argparse
from datetime import datetime
from typing import List, Dict
from typing import TypedDict, List

def read_html_files_to_dict(directory):
    html_files_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                file_key = os.path.splitext(filename)[0]
                html_files_dict[file_key] = file_content
    return html_files_dict


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


class ArticleContent(TypedDict):
    _id: str
    _body: str

class ArticleMeta(TypedDict):
    _id: str
    _title: str
    _createdAt: str
    _updatedAt: str
    _description: str
    _tags: List[str]
    _show: bool


def sync_articles(
    source_html_files,
    existing_meta_json: List[ArticleMeta],
    existing_content_json: List[ArticleContent],
):
    for source_file in source_html_files:
        # Check if the file already exists in the existing content JSON
        existing_content = next((item for item in existing_content_json if item["_id"] == source_file["id"]), None)
        if existing_content:
            if existing_content["_body"] != source_file["body"]:
                # Update the existing content with the new HTML body
                existing_content["_body"] = source_file["body"]
                # Update the corresponding meta information
                existing_meta = next((item for item in existing_meta_json if item["_id"] == source_file["id"]), None)
                if existing_meta:
                    existing_meta["_updatedAt"] = datetime.now().isoformat() + "Z"
        else:
            # Add new article
            current_date = datetime.now().isoformat() + "Z"
            existing_meta_json.append({
                "_id": source_file["id"],
                "_title": "",
                "_createdAt": current_date,
                "_updatedAt": current_date,
                "_description": "",
                "_tags": [],
                "_show": False
            })
            existing_content_json.append({
                "_id": source_file["id"],
                "_body": source_file["body"]
            })
    return existing_meta_json, existing_content_json


def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main(source_html_directory, aa_meta_json_path, aa_content_json_path):
    source_html_files_dict = read_html_files_to_dict(source_html_directory)
    current_date = datetime.now().isoformat()
    source_html_files_list = [
        {
            "id": file_key,
            "createdAt": current_date,
            "updatedAt": current_date,
            "body": file_content
        }
        for file_key, file_content in source_html_files_dict.items()
    ]

    existing_meta_json: List[ArticleMeta] = read_json_file(aa_meta_json_path)
    existing_content_json: List[ArticleContent] = read_json_file(aa_content_json_path)

    synced_meta_json, synced_content_json = sync_articles(
        source_html_files_list, existing_meta_json, existing_content_json
    )

    write_json_file(aa_meta_json_path, synced_meta_json)
    write_json_file(aa_content_json_path, synced_content_json)
    print("Synced meta JSON and content JSON files.")
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read HTML files from a directory into a dictionary.")
    parser.add_argument(
        "--html-dir",
        type=str,
        default="./converted_html",
        help="The path to the directory containing HTML files. Defaults to './converted_html'."
    )
    parser.add_argument(
        "--meta-json",
        type=str,
        default="../authored_articles_meta.json",
        help="The path to the authored_articles_meta.json file. Defaults to '../authored_articles_meta.json'."
    )
    parser.add_argument(
        "--content-json",
        type=str,
        default="../authored_articles_content.json",
        help="The path to the authored_articles_content.json file. Defaults to '../authored_articles_content.json'."
    )
    args = parser.parse_args()
    main(args.html_dir, args.meta_json, args.content_json)