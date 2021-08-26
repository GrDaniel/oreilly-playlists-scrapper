import json
from os import walk

from scrapper import OreillyPlaylistScrapper
from downloader import Downloader
from utils import cfg, collect_local_files


class BooksSynchronizer(object):

    def __init__(self):
        self.scrapper = OreillyPlaylistScrapper()
        self.downloader = Downloader()
        self.oreilly_collection = []
        self.books_to_download = []

    def sync_books(self):
        # self.fetch_playlists_collection()
        self.books_to_download = self.choose_books_to_download()

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




if __name__ == '__main__':
    synchronizer = BooksSynchronizer()
#    synchronizer.sync_books()
    synchronizer.choose_books_to_download()