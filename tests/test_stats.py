import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET

from scripts import profile_stats as stats
from scripts.render_profile import flight, stats as render_stats
from scripts.profile_themes import THEMES, variants


def repository(name, private=False, owner='Robin-G0'):
    return dict(name=name, full_name=f'{owner}/{name}', owner={'login': owner},
                private=private, default_branch='main', size=1)


def commit(oid, additions=4, deletions=2):
    return dict(oid=oid, additions=additions, deletions=deletions)


class CollectionTests(unittest.TestCase):
    def test_private_repositories_are_excluded_before_any_history_or_languages(self):
        private_name = 'never-read-this-private-repository'
        repos = [repository('public'), repository(private_name, True), repository('fork')]
        responses = [repos, {'C++': 800, 'Python': 200}, {'Python': 1000}]
        histories = [iter([commit('shared')]), iter([commit('shared'), commit('second', 10, 3)])]
        with patch.object(stats, 'api', side_effect=responses) as api, patch.object(stats, 'commits_for_repo', side_effect=histories) as history:
            data = stats.collect('Robin-G0')
        self.assertEqual(data['repositories'], 2)
        self.assertEqual(data['commits'], 2)
        self.assertEqual(data['lines_changed'], 19)
        self.assertEqual(data['languages'], {'Python': 1200, 'C++': 800})
        self.assertEqual(data['scope'], 'owned_public')
        self.assertNotIn(private_name, str(api.call_args_list))
        self.assertNotIn(private_name, str(history.call_args_list))
        for hidden in (private_name, 'second', 'shared', 'stars', 'forks'):
            self.assertNotIn(hidden, json.dumps(data))

    def test_repository_pagination_and_owner_filter(self):
        pages = [[repository(str(i)) for i in range(100)],
                 [repository('last'), repository('unrelated', owner='other')]]
        def fake_api(path):
            return pages.pop(0) if path.startswith('/users/') else {}
        with patch.object(stats, 'api', side_effect=fake_api), patch.object(stats, 'commits_for_repo', return_value=iter(())):
            self.assertEqual(stats.collect('Robin-G0')['repositories'], 101)

    def test_personal_tokens_are_ignored_and_local_calls_are_anonymous(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b'[]'
        with patch.dict(os.environ, {'GH_TOKEN': 'personal-secret', 'PROFILE_STATS_TOKEN': 'private-secret'}, clear=True), patch('urllib.request.urlopen', return_value=response) as request:
            self.assertEqual(stats.api('/users/Robin-G0/repos'), [])
        self.assertNotIn('Authorization', request.call_args.args[0].headers)

    def test_commit_pagination_pins_head_and_excludes_merges(self):
        first = [{'sha': f'{i:040x}', 'parents': [{}]} for i in range(99)]
        first.append({'sha': 'merge', 'parents': [{}, {}]})
        changes = {f'{i:040x}': (1, 2) for i in range(100)}
        with patch.object(stats, 'git', side_effect=[b'', b'fixed-head\n']), patch.object(stats, 'line_changes', return_value=changes), patch.object(stats, 'api', side_effect=[first, [{'sha': f'{99:040x}', 'parents': [{}]}]]) as api:
            result = list(stats.commits_for_repo(repository('repo'), 'Robin-G0'))
        self.assertEqual(len(result), 100)
        for call in api.call_args_list:
            query = parse_qs(urlsplit(call.args[0]).query)
            self.assertEqual(query['sha'], ['fixed-head'])
            self.assertEqual(query['author'], ['Robin-G0'])
        self.assertEqual(query['page'], ['2'])

    def test_empty_repo_and_incomplete_history(self):
        with patch.object(stats, 'api', return_value=[]), patch.object(stats, 'git') as git:
            self.assertEqual(list(stats.commits_for_repo(dict(repository('empty'), size=0), 'Robin-G0')), [])
            git.assert_not_called()
        with patch.object(stats, 'git', side_effect=[b'', b'head\n']), patch.object(stats, 'line_changes', return_value={}), patch.object(stats, 'api', return_value=[{'sha':'missing','parents':[{}]}]):
            with self.assertRaises(stats.CollectionError):
                list(stats.commits_for_repo(repository('repo'), 'Robin-G0'))

    def test_real_git_counts_root_additions_and_later_deletions(self):
        with tempfile.TemporaryDirectory() as tmp:
            def git(*args):
                return subprocess.run(['git', '-C', tmp, *args], check=True, capture_output=True).stdout.decode().strip()
            git('init', '--initial-branch=main')
            git('config', 'user.name', 'Test')
            git('config', 'user.email', 'test@example.invalid')
            git('config', 'core.autocrlf', 'false')
            path = Path(tmp) / 'sample.txt'
            path.write_bytes(b'one\ntwo\nthree\n')
            git('add', '.')
            git('commit', '-m', 'root')
            root = git('rev-parse', 'HEAD')
            path.write_bytes(b'one\nthree\n')
            git('commit', '-am', 'remove line')
            head = git('rev-parse', 'HEAD')
            self.assertEqual(stats.line_changes(tmp), {head: (0, 1), root: (3, 0)})


class DisplayTests(unittest.TestCase):
    def test_all_languages_shown_by_bytes_and_pending_is_not_zero(self):
        theme = variants(THEMES[0])['light']
        pending = render_stats(theme, stats.pending('Robin-G0'))
        self.assertIn('pending collection', pending)
        for hidden in ('stars', 'forks', 'private'):
            self.assertNotIn(hidden, pending)
        languages = {'C++': 800, 'Python': 200, **{f'Language {i}': 1 for i in range(8)}}
        data = dict(stats.pending('Robin-G0'), status='ready', updated='2026-11-12',
                    repositories=10, commits=1000, lines_changed=10000, languages=languages)
        svg = render_stats(theme, data)
        ET.fromstring(svg)
        for name in languages:
            self.assertIn(name, svg)
        self.assertIn('79.4%', svg)
        self.assertNotIn('Other', svg)

    def test_only_plane_moves_along_static_route(self):
        for identity in THEMES:
            svg = flight(variants(identity)['light'])
            self.assertNotIn('animation: signal', svg)
            self.assertNotIn('class="route"', svg)
            self.assertIn('offset-rotate: reverse', svg)
            root = ET.fromstring(svg)
            routes = [p for p in root.iter('{http://www.w3.org/2000/svg}path')
                      if p.get('d') == 'M 180 236 C 320 130 580 130 720 236']
            self.assertEqual(len(routes), 1)


if __name__ == '__main__':
    unittest.main()
