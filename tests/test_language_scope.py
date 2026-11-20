import unittest
from unittest.mock import patch

from scripts import profile_stats


class LanguageScopeTests(unittest.TestCase):
    def test_the_portfolio_site_counts_as_a_repository_but_not_in_language_shares(self):
        repos = [dict(name=name, full_name=f'Robin-G0/{name}', private=False, owner=dict(login='Robin-G0'))
                 for name in ('Motion-Input-Grid', 'Robin-G0.github.io')]
        def api(path):
            if path.startswith('/users/'):
                return repos
            return {'C++': 900, 'JavaScript': 100} if 'Motion-Input-Grid' in path else {'JavaScript': 50_000}
        with patch.object(profile_stats, 'api', side_effect=api) as calls,                 patch.object(profile_stats, 'commits_for_repo', return_value=[]):
            data = profile_stats.collect('Robin-G0')
        self.assertEqual(data['repositories'], 2)
        self.assertEqual(data['languages'], {'C++': 900, 'JavaScript': 100})
        self.assertNotIn('/repos/Robin-G0/Robin-G0.github.io/languages', [c.args[0] for c in calls.call_args_list])


if __name__ == '__main__':
    unittest.main()
