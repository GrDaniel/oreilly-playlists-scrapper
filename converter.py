import subprocess
import os
from dotenv import dotenv_values
from utils import EmptyDestinationPath
from pathlib import Path

config = dotenv_values(".env")


class EbookConverter():

    def __init__(self):
        self._coverter = 'ebook-convert'
        self._default_books_dir = os.path.dirname(os.path.abspath(__file__)) + "/safaribooks/Books"

    def convert_file_to_epub(self, book_name, book_id):
        original_file_path = "{}/{} ({})/{}.epub".format(self._default_books_dir, book_name, book_id, book_id)
        dest_dir = self.get_or_create_destination_dir()
        dest_file_path = "{}/{}.epub".format(dest_dir, book_name)
        subprocess.call([self._coverter, original_file_path, dest_file_path])

    def get_or_create_destination_dir(self):
        dest_dir_path = config.get('DEST_DIR')
        if dest_dir_path:
            Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
            return dest_dir_path
        else:
            raise EmptyDestinationPath
