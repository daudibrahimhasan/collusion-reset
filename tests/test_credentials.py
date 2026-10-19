import os
import unittest
from unittest.mock import Mock, patch

from collusion_reset.credentials import BoundedCompletion, groq_settings


class CredentialTests(unittest.TestCase):
    def settings(self):
        return {'model': 'groq/test-model', 'key': 'synthetic-secret',
                'slot': 'GROK_1', 'max_requests': 1}

    def test_explicit_selected_slot_and_no_secret_in_backend_settings(self):
        env = {'PATH': os.environ.get('PATH', ''),
               'LITELLM_LOCAL_MODEL_COST_MAP': 'True',
               'GROK_2': 'synthetic-secret', 'GROQ_KEY_SLOT': 'GROK_2',
               'GROQ_MODEL': 'groq/test-model', 'GROQ_MAX_REQUESTS': '1',
               'GROQ_FREE_TIER_CONFIRMED': 'true'}
        with patch.dict(os.environ, env, clear=True), patch('dotenv.load_dotenv'):
            self.assertEqual(groq_settings()['slot'], 'GROK_2')
            from collusion_reset.upstream_backend import UpstreamBackend
            backend = UpstreamBackend('groq/test-model')
            self.assertNotIn('synthetic-secret', str(backend.settings))
            self.assertFalse(backend.settings['account_fallback'])

    def test_upstream_episode_uses_selected_key_and_zero_retries(self):
        import tempfile
        from pathlib import Path
        env = {'PATH': os.environ.get('PATH', ''), 'GROK_1': 'synthetic-secret',
               'LITELLM_LOCAL_MODEL_COST_MAP': 'True',
               'GROQ_MODEL': 'groq/test-model', 'GROQ_FREE_TIER_CONFIRMED': 'true'}
        with patch.dict(os.environ, env, clear=True), patch('dotenv.load_dotenv'):
            from collusion_reset.upstream_backend import UpstreamBackend
            backend = UpstreamBackend('groq/test-model')
        completion = Mock(return_value='synthetic-response')
        backend.groq_completion.completion = completion
        def episode(**kwargs):
            from experiments import agents
            self.assertEqual(agents.LLM_MAX_RETRIES, 0)
            self.assertEqual(agents.completion(model='groq/test-model'), 'synthetic-response')
            return {'episode_id': 'synthetic', 'agents': {}}
        backend.run_episode = episode
        with tempfile.TemporaryDirectory() as root:
            backend.episode([{'task_type': 'data_search'}] * 2,
                            backend.initial_state(), Path(root), 0)
        self.assertEqual(completion.call_args.kwargs['api_key'], 'synthetic-secret')

    def test_missing_selected_key_does_not_fall_back(self):
        with patch.dict(os.environ, {'GROK_2': 'other-key'}, clear=True), patch('dotenv.load_dotenv'):
            with self.assertRaisesRegex(ValueError, 'GROK_1'):
                groq_settings()

    def test_billing_confirmation_required(self):
        with patch.dict(os.environ, {'GROK_1': 'test', 'GROQ_MODEL': 'groq/test'}, clear=True), \
                patch('dotenv.load_dotenv'):
            with self.assertRaisesRegex(ValueError, 'FREE_TIER_CONFIRMED'):
                groq_settings()

    def test_cap_enforced_without_extra_call(self):
        completion = Mock(return_value='response')
        bounded = BoundedCompletion(completion, self.settings())
        self.assertEqual(bounded(model='groq/test-model'), 'response')
        with self.assertRaisesRegex(RuntimeError, 'cap reached'):
            bounded(model='groq/test-model')
        completion.assert_called_once_with(model='groq/test-model',
                                           api_key='synthetic-secret', num_retries=0, timeout=60)

    def test_errors_redacted_and_no_fallback(self):
        completion = Mock(side_effect=RuntimeError('429 synthetic-secret'))
        bounded = BoundedCompletion(completion, self.settings())
        with self.assertRaises(RuntimeError) as error:
            bounded(model='groq/test-model')
        self.assertNotIn('synthetic-secret', str(error.exception))
        completion.assert_called_once()

    def test_other_model_blocked_before_network(self):
        completion = Mock()
        with self.assertRaisesRegex(RuntimeError, 'Model change'):
            BoundedCompletion(completion, self.settings())(model='groq/other')
        completion.assert_not_called()

    def test_preflight_does_not_construct_backend(self):
        from collusion_reset.run import main
        with patch('sys.argv', ['run']), patch('builtins.print'), \
                patch('collusion_reset.run.groq_settings', return_value=self.settings()), \
                patch('collusion_reset.upstream_backend.UpstreamBackend') as backend:
            main()
        backend.assert_not_called()


if __name__ == '__main__':
    unittest.main()
