import re


def extract_book_id_from_url(url):
    book_id_regex = "\/(\d+)\/$"
    return re.findall(book_id_regex, url)[0]
