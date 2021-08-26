import re
from dotenv import dotenv_values
from os import walk

cfg = dotenv_values(".env")


def extract_book_id_from_url(url):
    book_id_regex = "\/(\d+)\/$"
    return re.findall(book_id_regex, url)[0]


class EmptyDestinationPath(Exception):
    pass


def collect_local_files(dir_path):
    files = []
    for (a, b, filenames) in walk(dir_path):
        for filename in filenames:
            files.append(filename)
    return files
