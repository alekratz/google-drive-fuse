#/bin/env python2
__author__ = 'Alek Ratzloff <alekratz@gmail.com>'


import os
import os.path
import mimetypes
from apiclient.http import MediaFileUpload
from auth import OAuth2Session


GOOGLE_APPS_FOLDER='application/vnd.google-apps.folder'

class DriveStorage:
    def __init__(self, oauth2_session):
        """
        Creates a new Google Drive Storage object
        :param oauth2:
        :return:
        """
        self.oauth2 = oauth2_session
        self.files = [] # list of files in the drive storage unit
        self.folders = []

    def refresh_files(self):
        """
        Refreshes the list of files in the drive storage device
        """
        self.files = []
        self.folders = []
        service = self.oauth2.create_drive_service()
        files_list = service.files().list().execute()
        for file_metadata in files_list['items']:
            if file_metadata['mimeType'] == GOOGLE_APPS_FOLDER:
                self.folders += [file_metadata]
            else:
                self.files += [file_metadata]

        print 'loaded %d files' % len(self.files)
        print 'loaded %d folders' % len(self.folders)

    def save_file(self, path):
        """
        This is a wrapper method for save_new_file and update_file. If the path already exists, update_file is called;
        else save_new_file is called
        :param path:
        :return:
        """
        pass

    def save_new_file(self, path):
        title = os.path.basename(path)
        resource = {
            'title': title
        }
        service = self.oauth2.create_drive_service()
        # check https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/ for more info
        service.files().insert(
            body = resource,
            media_body = path
        ).execute()

    def update_file(self, path):
        title = os.path.basename(path)
        resource = {
            'title': title
        }
        service = self.oauth2.create_drive_service()
        service.files().update(
            body = resource,
            media_body = path
        ).execute()


if __name__ == '__main__':
    session = OAuth2Session()
    storage = DriveStorage(session)
    storage.refresh_files()