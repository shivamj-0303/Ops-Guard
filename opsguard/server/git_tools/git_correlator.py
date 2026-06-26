from git import Repo


def get_recent_commits(repo_path=".", limit=5):
    repo = Repo(repo_path)
    print(repo.working_tree_dir)

    commits = []

    for commit in repo.iter_commits(max_count=limit):
        files_changed = []

        if commit.parents:
            diffs = commit.diff(commit.parents[0])

            for diff in diffs:
                if diff.a_path:
                    files_changed.append(diff.a_path)

        commits.append({
            "hash": commit.hexsha[:8],
            "author": str(commit.author),
            "message": commit.message.strip(),
            "timestamp": str(commit.committed_datetime),
            "files_changed": files_changed
        })

    return commits