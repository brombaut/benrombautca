import os
import sys

# Pin pandoc to the binary bundled in the pinned pypandoc_binary wheel (#548).
# pypandoc otherwise searches PATH, ~/bin and its own bundle and uses the
# HIGHEST version it finds, so a newer pandoc installed anywhere on the machine
# silently takes over and the committed HTML becomes a function of the machine
# rather than of the markdown. PYPANDOC_PANDOC replaces that search entirely.
def pin_pandoc():
    import pypandoc

    bundled = os.path.join(
        os.path.dirname(os.path.realpath(pypandoc.__file__)), "files", "pandoc"
    )
    if not os.path.isfile(bundled):
        sys.exit(
            f"No bundled pandoc at {bundled}.\n"
            "Install the pinned toolchain: "
            "pip install -r src/blog/content/requirements.txt"
        )
    os.environ["PYPANDOC_PANDOC"] = bundled


def convert_md_to_html(md_file_path, html_file_path):
    import pypandoc

    # Convert Markdown to HTML using pandoc
    html_content = pypandoc.convert_file(md_file_path, 'html', extra_args=['-f', 'markdown-implicit_figures'])

    # Rewrite local image paths for deployed site
    html_content = html_content.replace('src="images/', 'src="blog-images/')

    # Only write when the output actually changed, so editing one post produces a
    # one-post diff instead of rewriting every converted file (#548).
    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            if html_file.read() == html_content:
                return False

    # Write the HTML content to a file
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    return True

def convert_directory(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # sorted() so the run order does not depend on the filesystem.
    # sources_md/archive/ holds the archived posts and is deliberately not
    # descended into: their HTML is frozen and is never reconverted (#548).
    for filename in sorted(os.listdir(source_dir)):
        if filename.endswith('.md'):
            md_file_path = os.path.join(source_dir, filename)
            html_file_name = filename.replace('.md', '.html')
            html_file_path = os.path.join(dest_dir, html_file_name)
            if convert_md_to_html(md_file_path, html_file_path):
                print(f"wrote {html_file_name}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Markdown files in a directory to HTML."
    )
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    parser.add_argument(
        "--source-dir",
        help="The source directory containing Markdown files.",
        default=os.path.join(script_dir, "sources_md"),
    )
    parser.add_argument(
        "--dest-dir",
        help="The destination directory for the converted HTML files.",
        default=os.path.join(script_dir, "converted_html"),
    )
    
    args = parser.parse_args()

    pin_pandoc()
    convert_directory(args.source_dir, args.dest_dir)
