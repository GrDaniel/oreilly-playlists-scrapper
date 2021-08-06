import dropbox
from dotenv import dotenv_values
from os import listdir, path

config = dotenv_values(".env")


class DropBoxClient():

    def __init__(self):
        self.dbx_api = dropbox.Dropbox(config.get('DROPBOX_TOKEN'))

    def upload_new_books(self):
        dropbox_folders = self._get_list_uploaded_folders()
        local_folders = self._get_list_local_folders()
        self._create_missing_dropbox_folders(dropbox_folders, local_folders)
        self._upload_books()



    def _get_list_uploaded_folders(self):
        all_objects = self._get_all_objects()
        return [obj.name for obj in all_objects if self._is_folder(obj)]

    def _get_list_local_folders(self):
        base_path = config.get('DEST_DIR')
        return [directory for directory in listdir(base_path) if path.isdir("{}/{}".format(base_path, directory))]

    def _get_all_objects(self):
        objects = self.dbx_api.files_list_folder(path=config.get('DROPBOX_DEST_DIR'))
        return objects.entries

    def _is_folder(self, obj):
        return True if isinstance(obj, dropbox.files.FolderMetadata) else False

    def _is_file(self, obj):
        return True if isinstance(obj, dropbox.files.FileMetadata) else False

    def _create_missing_dropbox_folders(self, dropbox_folders, local_folders):
        missing_folders = [folder for folder in local_folders if folder not in dropbox_folders]
        for folder in missing_folders:
            self._create_dropbox_folder(folder)
            print("Created missing DropBox folder: {} !!!".format(folder))

    def _create_dropbox_folder(self, folder_name):
        dropbox_base_path = config.get('DROPBOX_DEST_DIR')
        new_folder_path = f'{dropbox_base_path}{folder_name}'
        print("Creating a new DropBox directory...")
        print(f"New directory path: {new_folder_path}")
        self.dbx_api.files_create_folder_v2(new_folder_path)

    def _upload_books(self):
        new_books = self._get_new_books_list()

    def _get_new_books_list(self):
        uploaded_books = self._get_uploaded_books()
        local_books = self._get_local_books()
        new_books = [book for book in local_books if book not in uploaded_books]
        print(f"New books:{new_books}")
        return new_books

    def _get_uploaded_books(self):
        books = []

        all_objects = self._get_all_objects()
        books = [book for book in all_objects if self._is_file(book)]

if __name__ == "__main__":
    db = DropBoxClient()
    db.upload_new_books()