"""Inspect or checkpoint workflow state; does not approve scientific changes."""
import argparse
import json
from datetime import datetime, timezone
from research_support import ROOT, atomic_json, digest, read_json

STAGES = ('intake', 'discovery', 'analysis', 'synthesis', 'review', 'complete')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('status', 'checkpoint'))
    parser.add_argument('--stage', choices=STAGES)
    args = parser.parse_args()
    path = ROOT / 'workflow/STATE.json'
    try:
        state = read_json(path)
        if args.command == 'checkpoint':
            if args.stage:
                state['stage'] = args.stage
            state['project_sha256'] = digest(ROOT / 'PROJECT.md')
            state['updated_at'] = datetime.now(timezone.utc).isoformat()
            atomic_json(path, state)
        print(json.dumps(state, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')
