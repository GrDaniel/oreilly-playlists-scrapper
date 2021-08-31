import os
import subprocess
from pathlib import Path

from dotenv import dotenv_values

from utils import EmptyDestinationPath, PROJECT_DIR_PATH

config = dotenv_values(".env")


class EbookConverter(object):

    def __init__(self):
        self._coverter = 'ebook-convert'
        self._default_books_dir = PROJECT_DIR_PATH + "/safaribooks/Books"

    def convert_file_to_epub(self, book_name, book_id):
        print(f"Starting convert for file: {book_name} ...")
        original_file_path = self._find_original_file_path(book_id)
        dest_dir = self.get_or_create_destination_dir()
        dest_file_path = "{}/{}.epub".format(dest_dir, book_name)
        subprocess.call([self._coverter, original_file_path, dest_file_path])
        print("File convert finished!")

    def get_or_create_destination_dir(self):
        dest_dir_path = config.get('DEST_DIR')
        if dest_dir_path:
            Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
            return dest_dir_path
        else:
            raise EmptyDestinationPath

    def _find_original_file_path(self, book_id):
        dirs = os.listdir(self._default_books_dir)
        book_dir_name = None
        for dir_name in dirs:
            if book_id in dir_name:
                book_dir_name = dir_name
        if book_dir_name:
            return f"{self._default_books_dir}/{book_dir_name}/{book_id}.epub"
