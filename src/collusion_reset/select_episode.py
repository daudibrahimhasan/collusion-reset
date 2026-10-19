"""Reproduce Emi's fixed-seed schedule without changing its tasks or ordering.

Adapted from Emi's PR #2 (9d99195). Sampling order and RNG operations are unchanged.
"""

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import random

from collusion_reset.episode_smoke import ROOT, UPSTREAM, check_upstream

SEED = 42
CATALOG = UPSTREAM / 'task' / 'data-search' / 'task_manifest_data_search50.json'
APPROVED = ROOT / 'configs' / 'pilot-001.json'
# Dictionary order and the source catalog order are part of the original procedure.
SAMPLE_SIZES = {'support_escalation': 8, 'procurement_finance': 8,
                'clinical_safety': 7, 'campus_facilities': 7}


def select_episodes(tasks):
    if not isinstance(tasks, list) or len(tasks) != 50:
        raise ValueError('Expected the original 50-task catalog')
    families = defaultdict(list)
    seen = set()
    for task in tasks:
        if not isinstance(task, dict) or task.get('task_type') != 'data_search':
            raise ValueError('Expected data_search task records')
        task_id, family = task.get('task_id'), task.get('task_family')
        if not isinstance(task_id, str) or not task_id or task_id in seen:
            raise ValueError('Task IDs must be nonempty and unique')
        if family not in SAMPLE_SIZES:
            raise ValueError('Unexpected task family')
        seen.add(task_id)
        families[family].append(task_id)
    rng = random.Random(SEED)  # Fresh per invocation; importing never selects tasks.
    selected = []
    for family, count in SAMPLE_SIZES.items():
        if len(families[family]) < count:
            raise ValueError(f'Not enough tasks in {family}')
        selected.extend(rng.sample(families[family], count))
    rng.shuffle(selected)
    return {'pairs': [{'tasks': selected[i:i + 2]} for i in range(0, len(selected), 2)]}


def write_manifest(path, manifest):
    # Exclusive creation protects the agreed schedule and any existing output.
    with Path(path).open('x', encoding='utf-8') as output:
        json.dump(manifest, output, indent=2, ensure_ascii=False)
        output.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--output', type=Path, help='Create a NEW reproduction file; never overwrite')
    mode.add_argument('--check', type=Path, help='Compare an existing schedule without editing it')
    args = parser.parse_args()
    try:
        check_upstream()
        source = CATALOG.read_bytes()
        manifest = select_episodes(json.loads(source))
        if args.output:
            write_manifest(args.output, manifest)
            action = f'Created {args.output}'
        else:
            target = args.check or APPROVED
            if json.loads(target.read_text(encoding='utf-8')) != manifest:
                raise ValueError('Schedule differs from the original fixed-seed selection; no files changed')
            action = f'Exact task/role/order match: {target}'
        print(f'{action}\nSeed: {SEED}; tasks: 30; ordered pairs: 15')
        print(f'Catalog SHA-256: {sha256(source).hexdigest()}')
    except (OSError, ValueError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
