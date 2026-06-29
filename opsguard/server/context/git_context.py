from git import Repo


def collect_git_context(repo_path):
    repo = Repo(repo_path)

    return {
        "branch": repo.active_branch.name,
        "is_dirty": repo.is_dirty(),
        "head_commit": repo.head.commit.hexsha,
    }