import unittest

from collusion_reset.full_episode_probe import retry_details


class RetryDiagnosticTests(unittest.TestCase):
    def test_provider_wait_and_counts(self):
        counts, wait = retry_details(RuntimeError(
            'Limit 7000, Used 6718, Requested 6059. Please try again in 50.517142857s.'))
        self.assertEqual(counts, [7000, 6718, 6059])
        self.assertAlmostEqual(wait, 51.517142857)

    def test_oversized_single_request_is_visible(self):
        counts, _ = retry_details(RuntimeError('Limit 7000, Used 0, Requested 9500'))
        self.assertGreater(counts[2], counts[0])

    def test_actual_request_too_large_message_without_used(self):
        counts, wait = retry_details(RuntimeError(
            'Request too large on input tokens per minute (ITPM): Limit 7000, Requested 7375, reduce message size'))
        self.assertEqual(counts, [7000, None, 7375])
        self.assertIsNone(wait)

    def test_unknown_error_does_not_invent_wait_or_leak_text(self):
        self.assertEqual(retry_details(RuntimeError('synthetic-secret')), (None, None))
