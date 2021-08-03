import json
from safaribooks.safaribooks import SafariBooks
from types import SimpleNamespace
from dotenv import dotenv_values

config = dotenv_values(".env")


class Downloader():

    SAVED_BOOKS_FILENAME = "books.json"

    def __init__(self):
        self._books_to_download = self._read_saved_books()

    def _read_saved_books(self):
        with open(self.SAVED_BOOKS_FILENAME, 'r') as file:
            file_content = json.loads(file.read())
            return file_content

    def download_books(self):
        for book in self._books_to_download:
            book_id = book.get('book_id')
            call_args = self._prepare_namespace_object(book_id)
            SafariBooks(call_args)

    def _prepare_namespace_object(self, book_id):
        credentials = (config.get('AUTH_EMAIL_DOWNLOAD'), config.get('AUTH_PASSWORD_DOWNLOAD'))
        return SimpleNamespace(cred=credentials, bookid=book_id, no_cookies=False, kindle=True, log=False)


if __name__ == "__main__":
    downloader = Downloader()
    downloader.download_books()
