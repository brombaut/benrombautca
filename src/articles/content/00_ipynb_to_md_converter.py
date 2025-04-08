import os
import shutil 


NOTEBOOK_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/sources_notebooks"
MD_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/sources_md"
ASSETS_IMAGES_DIR = f"{NOTEBOOK_DIR}/images"
GH_IMAGES_PREFIX = "https://raw.githubusercontent.com/brombaut/benrombautca/main/src/articles/content/sources_notebooks/images"


def get_list_of_notebook_directories():
    result = list()
    for file in os.listdir(NOTEBOOK_DIR):
        d = os.path.join(NOTEBOOK_DIR, file)
        if os.path.isdir(d):
            result.append(d)
    return result


def copy_notebook_md(nb_dir, article_name):
    def read_file_as_str(path):
        with open(path, "r") as f:
            return f.read()
    def replace_image_paths_with_correct_path(md_str):
        search_str = f"![png]({article_name}_files"
        replace_str = f"![]({GH_IMAGES_PREFIX}/{article_name}"
        return md_str.replace(search_str, replace_str)
    def write_new_md_to_src_md(md_str):
        with open(f"{MD_DIR}/{article_name}.md", "w") as f:
            f.write(md_str)
    original_md = read_file_as_str(f"{nb_dir}/{article_name}.md")
    updated_md = replace_image_paths_with_correct_path(original_md)
    write_new_md_to_src_md(updated_md)


def copy_notebook_files_directory(nb_dir, article_name):
    articles_files_src_dir = f"{nb_dir}/{article_name}_files"
    if os.path.isdir(articles_files_src_dir):
        articles_files_dst_dir = f"{ASSETS_IMAGES_DIR}/{article_name}"
        if os.path.exists(articles_files_dst_dir):
            shutil.rmtree(articles_files_dst_dir)
        shutil.copytree(articles_files_src_dir, articles_files_dst_dir) 


def main():
    print("ipynb_to_md_syncer -- start")
    nb_dirs = get_list_of_notebook_directories()
    print(f"notebook directories to handle:")
    for d in nb_dirs:
        print(f"\t{d}")
    for nb_dir in nb_dirs:
        article_name = os.path.basename(os.path.normpath(nb_dir))
        # There should be 1 <article_name>.ipynb file, 1 <article_name>.md file, and 1 directory with the name <article_name>_files
        # which contains any images (so it might not actually be there)
        if not os.path.isfile(f"{nb_dir}/{article_name}.md"):
            return
        copy_notebook_md(nb_dir, article_name)
        copy_notebook_files_directory(nb_dir, article_name)
    print("ipynb_to_md_syncer -- done")

if __name__ == "__main__":
    main()
