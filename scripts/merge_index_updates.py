"""Validate an index proposal; writes only when --apply is passed."""
import argparse
from research_support import ROOT, merge_proposal

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('proposal')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        result = merge_proposal(ROOT, args.proposal, args.apply)
        print(f'{"Applied" if args.apply else "Validated"} proposal; {len(result)} indexed papers')
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')
