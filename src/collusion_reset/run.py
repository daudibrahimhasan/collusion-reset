"""Groq preflight (default), explicit one-episode smoke, or one reset trajectory."""

import argparse
import json
from pathlib import Path
import sys

from collusion_reset.credentials import groq_settings
from collusion_reset.episode_smoke import ROOT, UPSTREAM, check_upstream


def main():
    # Upstream progress uses Unicode arrows, including when piped on Windows.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['preflight', 'smoke', 'trajectory'], default='preflight')
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--trajectory-id')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        check_upstream()
        settings = groq_settings()
        if str(UPSTREAM) not in sys.path:
            sys.path.insert(0, str(UPSTREAM))
        from experiments.tasks import read_task_pairs
        manifest = args.manifest or ROOT / 'configs' / 'one-episode.json'
        pairs = read_task_pairs(manifest.resolve(), UPSTREAM)
        if not pairs or any(t.get('task_type') != 'data_search' for p in pairs for t in p):
            raise ValueError('Use nonempty upstream SQLite data_search task pairs')
        if args.stage == 'trajectory' and (not args.manifest or len(pairs) < 15):
            raise ValueError('Trajectory requires the reviewed --manifest with at least 15 pairs')
        print(json.dumps({'model': settings['model'], 'credential_slot': settings['slot'],
                          'max_requests': settings['max_requests'], 'task_pairs': len(pairs),
                          'account_fallback': False, 'live_calls_so_far': 0}, indent=2))
        if args.stage == 'preflight' or not args.execute:
            print('Offline preflight only. Provider access and model compatibility remain untested.')
            return
        if not args.output or args.output.exists():
            raise ValueError('Select a new --output directory; existing results are never overwritten')
        if args.stage == 'smoke' and len(pairs) != 1:
            raise ValueError('Smoke requires exactly one task pair')
        if args.stage == 'trajectory' and not args.trajectory_id:
            raise ValueError('Set a unique --trajectory-id')
        from collusion_reset.upstream_backend import UpstreamBackend
        from collusion_reset.study import episode_metrics, run_trajectory, save_json
        backend = UpstreamBackend(settings['model'])
        if args.stage == 'smoke':
            args.output.mkdir(parents=True, exist_ok=False)
            save_json(args.output / 'settings.json', backend.settings)
            save_json(args.output / 'status.json', {'status': 'running', 'mode': 'live-smoke-not-study'})
            try:
                result = backend.episode(pairs[0], backend.initial_state(), args.output, 0)
            except Exception as error:
                save_json(args.output / 'status.json', {'status': 'failed',
                          'error_type': type(error).__name__,
                          'completion_attempts': backend.groq_completion.attempted})
                raise
            save_json(args.output / 'episode.json', result)
            save_json(args.output / 'metrics.json', episode_metrics(result))
            save_json(args.output / 'status.json', {'status': 'complete',
                      'completion_attempts': backend.groq_completion.attempted})
        else:
            run_trajectory(backend, pairs, args.output, trajectory_id=args.trajectory_id,
                           order_seed=args.seed)
        print('Finished. Inspect raw records and usage before launching another run.')
    except (ValueError, OSError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
