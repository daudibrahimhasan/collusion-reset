"""Aggregate validated study manifests without treating episodes as replicates."""

import argparse
import csv
import json
from pathlib import Path

from collusion_reset.study import save_json, summarize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', nargs='+', help='Explicit study.json paths, not raw upstream runs')
    parser.add_argument('--output', required=True, help='New directory; never overwrite analysis')
    args = parser.parse_args()
    manifests = [json.loads(Path(p).read_text(encoding='utf-8')) for p in args.runs]
    summary = summarize(manifests)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / 'summary.json', summary)
    with (output / 'episodes.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['trajectory_id', 'mode', 'condition',
                                                    'episode_offset', 'valid',
                                                    'endpoint_version', 'source_file', 'mutual_accept', 'invalid_reasons',
                                                    'alice_correct', 'bob_correct'])
        writer.writeheader()
        for m in manifests:
            for condition, branch in m['branches'].items():
                for offset, e in enumerate(branch['episodes'], 1):
                    writer.writerow({'trajectory_id': m['trajectory_id'], 'mode': m['mode'],
                                     'condition': condition, 'episode_offset': offset,
                                     'valid': e['valid'],
                                     'endpoint_version': m['endpoint_version'],
                                     'source_file': e.get('source_file'),
                                     'mutual_accept': e['mutual_accept'],
                                     'invalid_reasons': ';'.join(e['invalid_reasons']),
                                     'alice_correct': e['task_correct']['alice'],
                                     'bob_correct': e['task_correct']['bob']})
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
