import os
from typing import Callable

from integration import util
from sh.contrib import git

from git import GitClient


class TestGitOperations:
    def test_git_clone(
        self,
        work_dir: str,
        git_client: GitClient,
    ):
        git_client.clone()
        assert len(os.listdir(work_dir)) > 0

    def test_git_push(
        self,
        git_remote: str,
        work_dir: str,
        work_clone_dir: str,
        create_file: Callable[[str], None],
        filetypes: list[str],
        git_client: GitClient,
    ):
        util.download_fn(create_file, filetypes)()
        git_client.push_all()

        git.clone(git_remote, work_clone_dir)
        util.assert_repos_equal(work_dir, work_clone_dir)
