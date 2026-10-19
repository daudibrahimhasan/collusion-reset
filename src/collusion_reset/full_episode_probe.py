"""One explicitly authorized episode with bounded same-key rate-limit waits.

Diagnostic launcher only. Never drops history, rotates keys or changes tasks.
"""

import argparse
import json
from pathlib import Path
import re
import sys
import time

from collusion_reset.episode_smoke import ROOT, UPSTREAM, check_upstream
from collusion_reset.study import episode_metrics, save_json


def retry_details(error):
    text = str(error)  # Parse locally; never persist raw provider errors.
    limit = re.search(r'Limit\s*:?\s*(\d+)', text, re.I)
    requested = re.search(r'Requested\s*:?\s*(\d+)', text, re.I)
    used = re.search(r'Used\s*:?\s*(\d+)', text, re.I)
    counts = ([int(limit.group(1)), int(used.group(1)) if used else None,
               int(requested.group(1))] if limit and requested else None)
    match = re.search(r'try again in ([0-9.]+)s', text)
    wait = float(match.group(1)) + 1 if match else None
    return counts, wait


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    check_upstream()
    from collusion_reset.credentials import groq_settings
    settings = groq_settings()
    args.output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(UPSTREAM))
    from experiments.tasks import read_task_pairs
    from collusion_reset.upstream_backend import UpstreamBackend
    backend = UpstreamBackend(settings['model'])
    original = backend.groq_completion.completion
    requests = []
    started = time.monotonic()

    def persist(status, **extra):
        save_json(args.output / 'probe-status.json', {
            'status': status, 'elapsed_seconds': round(time.monotonic() - started, 2),
            'http_attempts': len(requests), 'successful_calls': sum(r['success'] for r in requests),
            'input_tokens': sum(r.get('input_tokens', 0) for r in requests),
            'provider_output_tokens': sum(r.get('provider_output_tokens', 0) for r in requests),
            'total_tokens': sum(r.get('total_tokens', 0) for r in requests),
            **extra})
        save_json(args.output / 'http-attempts.json', requests)

    def paced(**kwargs):
        for retry in range(6):
            if len(requests) >= 100 or time.monotonic() - started > 2400:
                raise RuntimeError('Diagnostic request/time budget reached')
            record = {'attempt': len(requests) + 1, 'success': False}
            requests.append(record)
            try:
                response = original(**kwargs)
            except Exception as error:
                counts, wait = retry_details(error)
                status = getattr(error, 'status_code', None)
                record.update(status=status if type(status) is int else None,
                              limit_used_requested=counts, retry_seconds=wait)
                persist('running')
                print(json.dumps(record), flush=True)
                if status != 429:
                    raise RuntimeError('Provider rejected request; see safe diagnostic status') from None
                if counts and counts[2] > counts[0]:
                    raise RuntimeError('Single request exceeds account token-rate limit; waiting cannot fix it') from None
                if wait is None or wait > 120 or retry == 5:
                    raise RuntimeError('Rate-limit wait exceeds bounded diagnostic policy') from None
                time.sleep(wait)
            else:
                usage = response.usage
                record.update(success=True, input_tokens=usage.prompt_tokens,
                              provider_output_tokens=usage.completion_tokens,
                              total_tokens=usage.total_tokens)
                persist('running')
                print(json.dumps(record), flush=True)
                return response

    backend.groq_completion.completion = paced
    save_json(args.output / 'settings.json', {
        **backend.settings, 'diagnostic_same_key_retries': True,
        'http_attempt_cap': 100, 'elapsed_cap_seconds': 2400})
    persist('running')
    try:
        pairs = read_task_pairs(ROOT / 'configs' / 'one-episode.json', UPSTREAM)
        result = backend.episode(pairs[0], backend.initial_state(), args.output, 0)
        save_json(args.output / 'episode.json', result)
        save_json(args.output / 'metrics.json', episode_metrics(result))
    except Exception as error:
        # Error text is from the sanitizing adapter, not the raw provider exception.
        persist('failed', error_type=type(error).__name__)
        print('Episode incomplete; inspect probe-status.json and http-attempts.json', flush=True)
        return 1
    persist('complete')
    print('Complete episode saved, including grading, verdicts, feedback and reflection.', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
