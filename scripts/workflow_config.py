"""Read literal project configuration; never execute or interpolate .env values."""
import argparse
import json
import re
from research_support import ROOT


def load_config(root=ROOT):
    values = {}
    path = root / '.env'
    if path.exists():
        for number, line in enumerate(path.read_text().splitlines(), 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, sep, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if not sep or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
                raise ValueError(f'.env line {number}: expected KEY=value')
            if key in values:
                raise ValueError(f'.env line {number}: duplicate key {key}')
            if value.startswith(('"', "'")):
                if len(value) < 2 or value[-1] != value[0]:
                    raise ValueError(f'.env line {number}: unmatched quote')
                value = value[1:-1]
            else:
                value = re.split(r'\s+#', value, maxsplit=1)[0].rstrip()
            values[key] = value
    raw = values.get('MAX_PARALLEL_PAPERS', '3')
    if not re.fullmatch(r'[1-9][0-9]*', raw):
        raise ValueError('MAX_PARALLEL_PAPERS must be a positive integer')
    vault = values.get('OBSIDIAN_VAULT', '').strip()
    return {'obsidian_vault': None if vault in ('', 'your_vault') else vault,
            'max_parallel_papers': int(raw)}


def paper_capacity(state, config):
    requested = state['limits']['max_parallel_analysts']
    if type(requested) is not int or requested < 1:
        raise ValueError('Invalid max_parallel_analysts state limit')
    limit = min(requested, config['max_parallel_papers'])
    running = sum(task.get('role') == 'paper_analyst' and task.get('status') == 'running'
                  for task in state['tasks'])
    if running > limit:
        raise ValueError(f'{running} paper analysts running exceeds effective cap {limit}; reconcile active tasks before dispatch')
    return {'effective_max_parallel_papers': limit, 'running': running,
            'available_slots': limit - running}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-capacity', action='store_true')
    args = parser.parse_args()
    try:
        config = load_config()
        if args.check_capacity:
            from research_support import read_json
            print(json.dumps(paper_capacity(read_json(ROOT / 'workflow/STATE.json'), config), indent=2))
        else:
            # Only expose the two recognized settings, never unrelated .env values.
            print(json.dumps(config, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Error: {exc}\n')
