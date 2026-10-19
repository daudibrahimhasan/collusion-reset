from collections import Counter
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from collusion_reset.episode_smoke import ROOT, UPSTREAM
from collusion_reset.select_episode import APPROVED, CATALOG, SAMPLE_SIZES, select_episodes, write_manifest


class EpisodeSelectionTests(unittest.TestCase):
    def setUp(self):
        self.tasks = json.loads(CATALOG.read_text(encoding='utf-8'))
        self.approved = json.loads(APPROVED.read_text(encoding='utf-8'))

    def test_exact_agreed_schedule_and_repeatability(self):
        self.assertEqual(select_episodes(self.tasks), self.approved)
        self.assertEqual(select_episodes(self.tasks), self.approved)

    def test_counts_and_input_not_mutated(self):
        before = deepcopy(self.tasks)
        ids = [t for pair in select_episodes(self.tasks)['pairs'] for t in pair['tasks']]
        lookup = {t['task_id']: t['task_family'] for t in self.tasks}
        self.assertEqual(len(ids), 30)
        self.assertEqual(len(set(ids)), 30)
        self.assertEqual(Counter(lookup[t] for t in ids), SAMPLE_SIZES)
        self.assertEqual(self.tasks, before)

    def test_original_pr_algorithm_matches_independently(self):
        # Original PR procedure, independent of select_episodes and grouping code.
        import random
        rng = random.Random(42)
        ids = []
        for family, count in [('support_escalation', 8), ('procurement_finance', 8),
                              ('clinical_safety', 7), ('campus_facilities', 7)]:
            ids.extend(rng.sample([t['task_id'] for t in self.tasks
                                   if t['task_family'] == family], count))
        rng.shuffle(ids)
        self.assertEqual({'pairs': [{'tasks': ids[i:i + 2]} for i in range(0, 30, 2)]},
                         self.approved)

    def test_existing_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'schedule.json'
            write_manifest(path, self.approved)
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_manifest(path, {'pairs': []})
            self.assertEqual(path.read_bytes(), original)

    def test_rejects_bad_source_records(self):
        for field, value in [('task_id', self.tasks[1]['task_id']),
                             ('task_type', 'code'), ('task_family', 'unknown')]:
            modified = deepcopy(self.tasks)
            modified[0][field] = value
            with self.assertRaises(ValueError):
                select_episodes(modified)
        with self.assertRaises(ValueError):
            select_episodes(self.tasks[:-1])

    def test_import_from_other_directory_has_no_output_side_effect(self):
        with tempfile.TemporaryDirectory() as root:
            env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
            subprocess.run([sys.executable, '-c', 'import collusion_reset.select_episode'],
                           cwd=root, env=env, check=True, capture_output=True, text=True)
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_cli_from_other_directory_and_loader_compatibility(self):
        with tempfile.TemporaryDirectory() as root:
            env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
            result = subprocess.run([sys.executable, '-m', 'collusion_reset.select_episode'],
                                    cwd=root, env=env, check=True, capture_output=True, text=True)
            self.assertIn('Exact task/role/order match', result.stdout)
            self.assertEqual(list(Path(root).iterdir()), [])
        if str(UPSTREAM) not in sys.path:
            sys.path.insert(0, str(UPSTREAM))
        from experiments.tasks import read_task_pairs
        pairs = read_task_pairs(APPROVED, UPSTREAM)
        self.assertEqual(len(pairs), 15)
        self.assertTrue(all(t['task_type'] == 'data_search' for pair in pairs for t in pair))


if __name__ == '__main__':
    unittest.main()
