import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from collusion_reset.episode_smoke import UPSTREAM, check_upstream


@unittest.skipUnless(importlib.util.find_spec('litellm'), 'Requires isolated upstream runtime')
class UpstreamAdapterTests(unittest.TestCase):
    def test_actual_upstream_signature_and_reset_without_network(self):
        import sys
        check_upstream()
        if str(UPSTREAM) not in sys.path:
            sys.path.insert(0, str(UPSTREAM))
        from collusion_reset.upstream_backend import UpstreamBackend
        from experiments.models import EpisodeRunConfig
        import experiments.episode_runner as runner
        with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'synthetic-not-a-real-key'}):
            backend = UpstreamBackend('openrouter/example/model:free')
        state = backend.initial_state()
        original_system = state['alice'][0]['content']
        state['alice'] = []
        state['bob'].append({'role': 'user', 'content': 'retained-canary'})
        backend.restore_instructions(state)
        self.assertEqual(state['alice'][0]['content'], original_system)
        self.assertNotIn('retained-canary', str(state['alice']))
        self.assertIn('retained-canary', str(state['bob']))
        seen = {}
        def fake_episode(*, pair, agent_configs, repo_root, config, agent_messages):
            seen['config'] = config
            self.assertIsInstance(config, EpisodeRunConfig)
            self.assertEqual(repo_root, UPSTREAM)
            with self.assertRaisesRegex(RuntimeError, 'history dropping forbidden'):
                runner._drop_oldest_cross_episode_block()
            return {'episode_id': 'fixture-id', 'agents': {},
                    'channel_transcript': [{'content': 'payload', 'message_type': 'unmetered-label'}]}
        backend.run_episode = fake_episode
        with tempfile.TemporaryDirectory() as root:
            result = backend.episode([{'task_type': 'data_search'}] * 2,
                                     state, Path(root), 3)
        self.assertEqual(result['char_limit'], 200)
        self.assertEqual(result['channel_transcript'][0]['message_type'], 'unmetered-label')
        self.assertTrue(seen['config'].reflection)
        self.assertTrue(seen['config'].reward)
        self.assertEqual(seen['config'].episode_index, 3)


if __name__ == '__main__':
    unittest.main()
