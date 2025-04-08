import pypandoc
import os
import argparse

def convert_md_to_html(md_file_path, html_file_path):
    # Ensure pandoc is installed
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()
    
    # Convert Markdown to HTML using pandoc
    html_content = pypandoc.convert_file(md_file_path, 'html')
    
    # Write the HTML content to a file
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def convert_directory(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.md'):
            md_file_path = os.path.join(source_dir, filename)
            html_file_name = filename.replace('.md', '.html')
            html_file_path = os.path.join(dest_dir, html_file_name)
            convert_md_to_html(md_file_path, html_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Markdown files in a directory to HTML."
    )
    parser.add_argument(
        "--source-dir",
        help="The source directory containing Markdown files.",
        default="./sources_md",
    )
    parser.add_argument(
        "--dest-dir",
        help="The destination directory for the converted HTML files.",
        default="./converted_html",
    )
    
    args = parser.parse_args()
    
    convert_directory(args.source_dir, args.dest_dir)
