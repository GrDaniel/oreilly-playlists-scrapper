from safaribooks.safaribooks import SafariBooks
from types import SimpleNamespace
from dotenv import dotenv_values

config = dotenv_values(".env")


class Downloader(object):

    def download_book(self, book_id):
        call_args = self.prepare_namespace_object(book_id)
        SafariBooks(call_args)

    @staticmethod
    def prepare_namespace_object(book_id):
        credentials = (config.get('AUTH_EMAIL_DOWNLOAD'), config.get('AUTH_PASSWORD_DOWNLOAD'))
        return SimpleNamespace(cred=credentials, bookid=book_id, no_cookies=False, kindle=True, log=False)


if __name__ == "__main__":
    downloader = Downloader()
    downloader.download_book()
