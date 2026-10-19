from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from collusion_reset.study import FixtureBackend, episode_metrics, run_trajectory, summarize


class StudyTests(unittest.TestCase):
    def run_fixture(self, root, backend=None, **kwargs):
        return run_trajectory(backend or FixtureBackend(), list(range(15)), Path(root) / 'run',
                              trajectory_id='fixture-1', **kwargs)

    def test_full_checkpoint_branch_and_disk_roundtrip(self):
        with tempfile.TemporaryDirectory() as root:
            result = self.run_fixture(root)
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(len(result['prefix']), 3)
            self.assertEqual(len(result['branches']), 4)
            self.assertEqual(len({b['future_pairs_sha256'] for b in result['branches'].values()}), 1)
            for branch in result['branches'].values():
                self.assertEqual(len(branch['episodes']), 5)
            checkpoint = json.loads((Path(root) / 'run/checkpoint.json').read_text())
            self.assertEqual(len(checkpoint['history_a']), 4)
            self.assertEqual(result, json.loads((Path(root) / 'run/study.json').read_text()))
            with self.assertRaises(FileExistsError):
                self.run_fixture(root)

    def test_reset_only_once_and_same_future_pairs(self):
        class Recording(FixtureBackend):
            def __init__(self):
                self.seen = []
            def episode(self, pair, histories, output, index):
                self.seen.append((output.name, pair, deepcopy(histories)))
                return super().episode(pair, histories, output, index)
        backend = Recording()
        with tempfile.TemporaryDirectory() as root:
            self.run_fixture(root, backend)
        for condition, expected in [('continue', (4, 4)), ('reset_a', (1, 4)),
                                    ('reset_b', (4, 1)), ('reset_both', (1, 1))]:
            calls = [c for c in backend.seen if c[0] == condition]
            self.assertEqual([c[1] for c in calls], list(range(3, 8)))
            self.assertEqual(tuple(len(calls[0][2][a]) for a in ('alice', 'bob')), expected)
            self.assertEqual(tuple(len(calls[1][2][a]) for a in ('alice', 'bob')),
                             tuple(n + 1 for n in expected))

    def test_ineligible_is_recorded(self):
        class Reject(FixtureBackend):
            def episode(self, *args):
                result = super().episode(*args)
                result['agents']['alice']['verdict'] = 'reject'
                result['agents']['alice']['verdict_submission']['verdict'] = 'reject'
                return result
        with tempfile.TemporaryDirectory() as root:
            result = self.run_fixture(root, Reject())
        self.assertEqual(result['status'], 'ineligible')
        self.assertEqual(len(result['prefix']), 10)
        self.assertEqual(result['branches'], {})

    def test_failure_is_preserved_without_claiming_completion(self):
        class Broken(FixtureBackend):
            def episode(self, *args):
                raise RuntimeError('fixture failure')
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(RuntimeError):
                self.run_fixture(root, Broken())
            result = json.loads((Path(root) / 'run/study.json').read_text())
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['error_type'], 'RuntimeError')

    def test_mutual_accept_does_not_depend_on_log_size(self):
        backend = FixtureBackend()
        result = backend.episode(None, backend.initial_state(), None, 0)
        self.assertTrue(episode_metrics(result)['mutual_accept'])
        result['agents']['alice']['verdict_forced'] = True
        self.assertIsNone(episode_metrics(result)['mutual_accept'])
        result['agents']['alice']['verdict_forced'] = False
        result['agents']['bob']['private_raw_log'] = []
        self.assertTrue(episode_metrics(result)['mutual_accept'])
        self.assertIsNone(episode_metrics(result)['evidence_compliance']['alice'])

    def test_message_type_can_carry_log_without_changing_behavioral_metric(self):
        backend = FixtureBackend()
        result = backend.episode(None, backend.initial_state(), None, 0)
        result['channel_transcript'] = [{'sender': 'bob', 'receiver': 'alice',
                                          'content': '', 'message_type': 'x' * 10000}]
        metrics = episode_metrics(result)
        self.assertTrue(metrics['mutual_accept'])
        self.assertNotIn('unsupported_mutual_approval', metrics)
        self.assertEqual(metrics['evidence_compliance'], {'alice': None, 'bob': None})

    def test_correctness_is_separate_from_mutual_accept(self):
        backend = FixtureBackend()
        result = backend.episode(None, backend.initial_state(), None, 0)
        result['agents']['alice']['expected_verdict'] = 'fail'
        result['agents']['bob'].pop('data_search_artifact')
        result['agents']['bob'].pop('expected_verdict')
        metrics = episode_metrics(result)
        self.assertTrue(metrics['mutual_accept'])
        self.assertEqual(metrics['task_correct'], {'alice': False, 'bob': None})

    def test_malformed_or_missing_verdict_is_unknown(self):
        backend = FixtureBackend()
        for change in ('missing', 'mismatch', 'controlled'):
            result = backend.episode(None, backend.initial_state(), None, 0)
            if change == 'missing':
                result['agents']['bob'].pop('verdict')
            elif change == 'mismatch':
                result['agents']['bob']['verdict_submission']['verdict'] = 'reject'
            else:
                result['controlled_bob'] = {'verdict': 'accept'}
            self.assertIsNone(episode_metrics(result)['mutual_accept'])

    def test_legacy_data_is_not_silently_relabelled(self):
        with self.assertRaisesRegex(ValueError, 'Legacy'):
            summarize([{'schema_version': 1}])

    def test_forced_episode_interrupts_checkpoint_streak(self):
        class ForcedSecond(FixtureBackend):
            def episode(self, pair, histories, output, index):
                result = super().episode(pair, histories, output, index)
                if output.name == 'prefix' and index == 1:
                    result['agents']['bob']['verdict_forced'] = True
                return result
        with tempfile.TemporaryDirectory() as root:
            result = self.run_fixture(root, ForcedSecond())
        self.assertEqual(len(result['prefix']), 5)
        self.assertIsNone(result['prefix'][1]['metrics']['mutual_accept'])

    def test_voluntary_reject_is_false_not_unknown(self):
        backend = FixtureBackend()
        result = backend.episode(None, backend.initial_state(), None, 0)
        result['agents']['bob']['verdict'] = 'reject'
        result['agents']['bob']['verdict_submission']['verdict'] = 'reject'
        self.assertIs(episode_metrics(result)['mutual_accept'], False)

    def test_unknown_tail_excluded_not_imputed(self):
        with tempfile.TemporaryDirectory() as root:
            result = self.run_fixture(root)
        result['branches']['reset_b']['episodes'][0]['mutual_accept'] = None
        summary = summarize([result])
        self.assertEqual(summary['comparisons']['reset_b']['paired_n'], 0)
        self.assertIsNone(summary['comparisons']['reset_b']['mean_difference'])
        self.assertEqual(summary['comparisons']['reset_a']['paired_n'], 1)

    def test_short_schedule_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                run_trajectory(FixtureBackend(), [], Path(root) / 'run', trajectory_id='x')
            self.assertFalse((Path(root) / 'run').exists())

    def test_summary_uses_paired_trajectory_not_episode_count(self):
        with tempfile.TemporaryDirectory() as root:
            first = self.run_fixture(root)
        second = deepcopy(first)
        second['trajectory_id'] = 'fixture-2'
        for e in second['branches']['reset_both']['episodes']:
            e['mutual_accept'] = False
        summary = summarize([first, second], bootstrap=100)
        self.assertEqual(summary['comparisons']['reset_both']['paired_n'], 2)
        self.assertEqual(summary['comparisons']['reset_both']['mean_difference'], -.5)
        self.assertEqual(summary['comparisons']['reset_a']['mean_difference'], 0)
        with self.assertRaises(ValueError):
            summarize([first, first])
        second['mode'] = 'live-pilot-not-main-study'
        with self.assertRaises(ValueError):
            summarize([first, second])


if __name__ == '__main__':
    unittest.main()
