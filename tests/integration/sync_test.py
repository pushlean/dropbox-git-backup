from typing import Callable

from integration import util
from integration.util import download_fn
from sh.contrib import git

from dropbox import DropboxClient
from sync import SyncManager


class TestSyncFullCycle:
    def test_first_sync(
        self,
        git_remote: str,
        work_dir: str,
        work_clone_dir: str,
        create_file: Callable[[str], None],
        filetypes: list[str],
        dropbox_client: DropboxClient,
        sync_manager: SyncManager,
    ):
        orig_download = dropbox_client.download
        dropbox_client.download = download_fn(create_file, filetypes)
        sync_manager.sync()

        git.clone(git_remote, work_clone_dir)
        util.assert_repos_equal(work_dir, work_clone_dir)
        dropbox_client.download = orig_download

    def test_sync_again(
        self,
        git_remote: str,
        work_dir: str,
        work_clone_dir: str,
        create_file: Callable[[str], None],
        filetypes: list[str],
        dropbox_client: DropboxClient,
        sync_manager: SyncManager,
    ):
        orig_download = dropbox_client.download
        dropbox_client.download = download_fn(create_file, filetypes, file_prefix="another")
        sync_manager.sync()

        git.clone(git_remote, work_clone_dir)
        util.assert_repos_equal(work_dir, work_clone_dir)
        dropbox_client.download = orig_download
