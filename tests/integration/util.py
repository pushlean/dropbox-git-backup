import os


def assert_repos_equal(expected_repo_path: str, actual_repo_path: str):
    assert os.listdir(expected_repo_path) == os.listdir(actual_repo_path)


def download_fn(create_file, filetypes: list[str], file_prefix: str = "test"):
    def _download():
        for filetype in filetypes:
            create_file(f"{file_prefix}.{filetype}")

    return _download
