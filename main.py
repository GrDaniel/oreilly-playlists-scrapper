import json
import logging

from converter import EbookConverter
from downloader import Downloader
from scrapper import OreillyPlaylistScrapper
from uploader import DropBoxClient
from utils import cfg, collect_local_files, PROJECT_DIR_PATH


class BooksSynchronizer(object):

    def __init__(self):
        logging.basicConfig(filename='BooksSynchronizer.log', level=logging.INFO)

        self.scrapper = OreillyPlaylistScrapper()
        self.downloader = Downloader()
        self.converter = EbookConverter()
        self.uploader = DropBoxClient()

        self.oreilly_collection = []
        self.new_books = []

    def sync_books(self):
        logging.info(f"***START***")
        self.fetch_playlists_collection()
        self.new_books = self.choose_books_to_download()
        logging.info(f"New books found: {len(self.books)}")
        logging.info(f"New books to download: {self.new_books}")
        self.download_and_convert_books()
        self.upload_books()
        logging.info(f"***END***")

    def fetch_playlists_collection(self):
        self.scrapper.get_books()

    def choose_books_to_download(self):
        self.oreilly_collection = self.read_books_collection()
        oreilly_books = [book.get('book_name') for book in self.oreilly_collection]
        local_collection = [filename.split(".")[0] for filename in collect_local_files(cfg.get('DEST_DIR'))]
        return [book for book in oreilly_books if book not in local_collection]

    @staticmethod
    def read_books_collection():
        with open('books.json', 'r') as file:
            return json.load(file)

    def download_and_convert_books(self):
        for book_name in self.new_books:
            book_id = self._get_book_id(book_name)
            self.downloader.download_book(book_id)
            self.converter.convert_file_to_epub(book_name, book_id)

    def _get_book_id(self, book_name):
        for book in self.oreilly_collection:
            if book.get('book_name') == book_name:
                return book.get('book_id')

    def upload_books(self):
        for book_name in self.new_books:
            src_path, dst_path = self._build_file_paths(book_name)
            logging.info(f"Uploading file {book_name} ...")
            self.uploader.upload_file(src_path, dst_path)
            logging.info(f"File {book_name} uploaded!")

    def _build_file_paths(self, book_name):
        playlist = self.read_book_details_from_cfg(book_name)
        src_path = f"{PROJECT_DIR_PATH}/converted_books/{book_name}.epub"
        dbx_base_url = cfg.get('DROPBOX_DEST_DIR')
        dst_path = f"{dbx_base_url}{playlist}/{book_name}.epub"
        return src_path, dst_path

    def read_book_details_from_cfg(self, book_name):
        for book in self.oreilly_collection:
            if book.get('book_name') == book_name:
                return book.get('playlist_name')


if __name__ == '__main__':
    synchronizer = BooksSynchronizer()
    synchronizer.sync_books()
