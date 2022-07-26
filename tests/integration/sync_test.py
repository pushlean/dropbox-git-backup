import os
import pathlib
import shutil
from typing import Callable

import pytest
from sh.contrib import git

from dropbox import DropboxClient
from git import GitClient
from sync import SyncManager


@pytest.fixture(scope="class")
def data_root_dir():
    data_root_dir = os.getenv("DATA_ROOT_DIR", "/tmp/dropbox-git-backup")
    pathlib.Path(data_root_dir).mkdir(parents=True, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(data_root_dir)
    yield data_root_dir
    os.chdir(cwd)
    shutil.rmtree(data_root_dir)


@pytest.fixture(scope="class")
def work_dir(data_root_dir: str):
    work_dir_path = os.path.join(data_root_dir, "test_folder")
    return work_dir_path


@pytest.fixture(scope="class")
def work_clone_dir(data_root_dir: str):
    work_dir_path = os.path.join(data_root_dir, "test_folder_clone")
    return work_dir_path


@pytest.fixture(scope="class")
def git_remote(work_dir: str, data_root_dir: str):
    work_dir_base = os.path.basename(work_dir)
    remote_dir = os.path.join(data_root_dir, f"{work_dir_base}.git")
    git.init("--bare", remote_dir)
    return remote_dir


@pytest.fixture(scope="package")
def git_author_email():
    return os.getenv("GIT_AUTHOR_EMAIL", "test@test.com")


@pytest.fixture(scope="package")
def git_author_name():
    return os.getenv("GIT_AUTHOR_NAME", "Test McGee")


@pytest.fixture(scope="class")
def filetypes() -> list[str]:
    return ["md", "png"]


@pytest.fixture(scope="class")
def create_file(work_dir: str) -> Callable[[str], None]:
    def _create(filetype: str):
        path = os.path.join(work_dir, f"test.{filetype}")
        with open(path, "w") as f:
            f.write(f"test {filetype}")

    return _create


def _download_fn(create_file, filetypes: list[str]):
    def _download():
        for filetype in filetypes:
            create_file(filetype)

    return _download


def assert_repos_equal(expected_repo_path: str, actual_repo_path: str):
    assert os.listdir(expected_repo_path) == os.listdir(actual_repo_path)


class TestSyncFullCycle:
    def test_init_git_repo(
        self,
        git_remote: str,
        work_dir: str,
        work_clone_dir: str,
        data_root_dir: str,
        create_file: Callable[[str], None],
        filetypes: list[str],
        git_author_email: str,
        git_author_name: str,
    ):
        git_client = GitClient(
            remote=git_remote,
            work_dir=work_dir,
            data_root_dir=data_root_dir,
            author_email=git_author_email,
            author_name=git_author_name,
        )
        dropbox_client = DropboxClient()
        dropbox_client.download = _download_fn(create_file, filetypes)
        sync_mgr = SyncManager(git_client=git_client, dropbox_client=dropbox_client)
        sync_mgr.sync()

        # Validate remote
        git.clone(git_remote, work_clone_dir)
        assert_repos_equal(work_dir, work_clone_dir)
