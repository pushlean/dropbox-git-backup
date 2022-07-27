import os
from datetime import datetime

from sh.contrib import git


class GitClient:
    def __init__(self, remote: str, work_dir: str, data_root_dir: str, author_email: str, author_name: str):
        self._remote = remote
        self._work_dir = work_dir
        self._data_root_dir = data_root_dir
        self._author_email = author_email
        self._author_name = author_name

        env = {}
        self._git = git.bake(_env=env)

    def clone(self):
        os.chdir(self._data_root_dir)
        git_dir = os.path.join(self._data_root_dir, "git")
        git.clone("--separate-git-dir", git_dir, self._remote, self._work_dir)
        os.chdir(self._work_dir)
        git.config("user.email", self._author_email)
        git.config("user.name", self._author_name)

    def _is_repo_dirty(self) -> bool:
        out = git.status("--short")
        return out != ""

    def push_all(self) -> None:
        os.chdir(self._work_dir)
        if not self._is_repo_dirty():
            return

        git.add(".")
        commit_message = self._create_commit_message()
        git.commit("--message", commit_message)
        git.push()

    def _create_commit_message(self) -> str:
        now = datetime.utcnow().isoformat()
        return f"Backup {now}"
