import dropbox
from dotenv import dotenv_values

config = dotenv_values(".env")


class DropBoxClient():

    def __init__(self):
        self.dbx_api = dropbox.Dropbox(config.get('DROPBOX_TOKEN'))

    def upload_file(self, src_path, dest_path):
        file = self._prepare_file_to_upload(src_path)
        self.dbx_api.files_upload(f=file, path=dest_path)

    @staticmethod
    def prepare_file_to_upload(src_path):
        with open(src_path, 'rb') as file:
            return file.read()


if __name__ == "__main__":
    db = DropBoxClient()
    db.upload_file()
