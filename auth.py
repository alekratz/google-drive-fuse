__author__ = 'Alek Ratzloff <alekratz@gmail.com>'

import httplib2
import os
import os.path
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage


CLIENT_ID = '160463896594-ff4pscki49ruol115iddp4i8fqm084ph.apps.googleusercontent.com'
CLIENT_SECRET = '4fgN-MMiW1krmaZ8sWVj1y_j'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'


class OAuth2Session:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.oauth_scope = OAUTH_SCOPE
        self.redirect_uri = REDIRECT_URI
        credentials_dir = os.path.join(os.getenv('HOME'), '.drive-fuse')
        if not os.path.exists(credentials_dir):
            os.mkdir(credentials_dir, 0700)
        self.credentials_file = os.path.join(credentials_dir, 'credentials')
        self._credentials = None

    def get_credentials(self):
        # get whether credentials have been defined or not
        if not self._credentials:
            storage = Storage(self.credentials_file)
            self._credentials = storage.get()
            # get whether credentials have been stored or not
            if not self._credentials:
                flow = OAuth2WebServerFlow(self.client_id, self.client_secret, self.oauth_scope, self.redirect_uri)
                authorize_url = flow.step1_get_authorize_url()
                print 'Go to the following link in your web browser: ' + authorize_url
                code = raw_input("Enter the code here: ")
                self._credentials = flow.step2_exchange(code)
                storage.put(self._credentials)
        elif self._credentials.access_token_expired:
            # gets if the access token has expired
            http = httplib2.Http()
            self._credentials.refresh(http) # force refresh of the access token
        return self._credentials

    def create_http_session(self):
        """
        Creates a HTTP session for the Google Drive API
        :return:
        """
        credentials = self.get_credentials()
        # get whether or not we've gotten credentials yet
        http = httplib2.Http()
        return credentials.authorize(http)

    def create_drive_service(self):
        # get the credentials, then create the service
        http = self.create_http_session()
        return build('drive', 'v2', http=http)