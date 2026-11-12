"""Collect owned PUBLIC repositories only, without a personal access token."""

from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.error import URLError
from urllib.parse import quote, urlencode
import urllib.request


class CollectionError(RuntimeError):
    """A refresh must fail instead of publishing incomplete totals."""


def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Robin-G0-profile'}
    # CI supplies only its short-lived, repository-scoped Actions token.
    # Personal-token variables (PROFILE_STATS_TOKEN, GH_TOKEN) are never read.
    if token := os.environ.get('PUBLIC_API_TOKEN'):
        headers['Authorization'] = f'Bearer {token}'
    request = urllib.request.Request('https://api.github.com' + path, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except (URLError, ValueError, TimeoutError):
        raise CollectionError('Public GitHub collection failed. Retry later; saved statistics were preserved.') from None


def git(*args):
    # Public bare clones need neither credentials nor a working tree.
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GIT_CONFIG_NOSYSTEM='1',
               GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C')
    try:
        return subprocess.run(['git', '-c', 'credential.helper=', *args], env=env,
                              check=True, capture_output=True, timeout=600).stdout
    except (OSError, subprocess.SubprocessError):
        raise CollectionError('Public repository history could not be read; no partial totals were published.') from None


def line_changes(bare):
    """Get added/deleted lines per non-merge SHA, without file contents."""
    output = git('-C', str(bare), 'log', '--no-merges', '--no-ext-diff', '--no-textconv',
                 '--format=commit:%H', '--shortstat', 'HEAD').decode('utf-8', errors='replace')
    changes = {}
    current = None
    for line in output.splitlines():
        if re.fullmatch(r'commit:[0-9a-f]{40,64}', line):
            current = line[7:]
            changes[current] = (0, 0)
        elif current and ('insertion' in line or 'deletion' in line):
            additions = re.search(r'(\d+) insertions?\(\+\)', line)
            deletions = re.search(r'(\d+) deletions?\(-\)', line)
            changes[current] = (int(additions[1]) if additions else 0,
                                int(deletions[1]) if deletions else 0)
    return changes


def commits_for_repo(repo, author):
    """Filter default-branch history to commits associated with the GitHub user."""
    if repo.get('size') == 0:
        if not api(f"/repos/{repo['full_name']}/branches?per_page=1"):
            return
    with tempfile.TemporaryDirectory(prefix='profile-public-') as tmp:
        bare = Path(tmp) / 'history.git'
        url = f"https://github.com/{repo['full_name']}.git"
        git('clone', '--bare', '--single-branch', '--branch', repo['default_branch'],
            '--', url, str(bare))
        head = git('-C', str(bare), 'rev-parse', 'HEAD').decode().strip()
        changes = line_changes(bare)
        page = 1
        while True:
            query = urlencode(dict(sha=head, author=author, per_page=100, page=page))
            batch = api(f"/repos/{repo['full_name']}/commits?{query}")
            for commit in batch:
                sha = commit['sha']
                if sha in changes and len(commit['parents']) <= 1:
                    additions, deletions = changes[sha]
                    yield dict(oid=sha, additions=additions, deletions=deletions)
                elif len(commit['parents']) <= 1:
                    raise CollectionError('Public history was incomplete; no partial totals were published.')
            if len(batch) < 100:
                return
            page += 1


def collect(user):
    repos = []
    page = 1
    while True:
        batch = api(f'/users/{quote(user, safe="")}/repos?type=owner&per_page=100&page={page}')
        # Even if authentication is accidentally supplied, exclude private data.
        repos.extend(r for r in batch if not r['private'] and
                     r['owner']['login'].casefold() == user.casefold())
        if len(batch) < 100:
            break
        page += 1
    languages = Counter()
    seen = set()
    additions = deletions = 0
    for repo in repos:
        languages.update(api(f"/repos/{repo['full_name']}/languages"))
        for commit in commits_for_repo(repo, user):
            if commit['oid'] in seen:
                continue
            seen.add(commit['oid'])
            additions += commit['additions']
            deletions += commit['deletions']
    return dict(schema=3, status='ready', user=user,
                updated=datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                repositories=len(repos), commits=len(seen), additions=additions,
                deletions=deletions, lines_changed=additions + deletions,
                languages=dict(sorted(languages.items(), key=lambda item: (-item[1], item[0]))),
                language_unit='bytes', scope='owned_public',
                history='authored_non_merge_commits_on_default_branches_deduplicated')


def pending(user):
    return dict(schema=3, status='awaiting_collection', user=user, updated=None,
                repositories=None, commits=None, additions=None, deletions=None,
                lines_changed=None, languages={}, language_unit='bytes', scope='owned_public',
                history='authored_non_merge_commits_on_default_branches_deduplicated')
