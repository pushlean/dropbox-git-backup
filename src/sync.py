from dropbox import DropboxClient
from git import GitClient


class SyncManager:
    def __init__(self, git_client: GitClient, dropbox_client: DropboxClient):
        self._git_client = git_client
        self._dbx_client = dropbox_client

    def sync(self):
        self._git_client.clone()
        self._dbx_client.download()
        self._git_client.push_all()
