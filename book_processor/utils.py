import os
import re
import json
from slugify import slugify

def get_book_meta(book_folder):
    match = re.match(r"(\d+)-\((.+)\)", book_folder)
    if match:
        book_id = int(match.group(1))
        title = match.group(2)
        slug = slugify(title)
        return {'id': book_id, 'title': title, 'slug': slug}
    return None

def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
