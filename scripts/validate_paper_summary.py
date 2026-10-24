"""Check summary structure, not scientific correctness."""
import argparse
from research_support import validate_summary

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('summary')
    args = parser.parse_args()
    try:
        validate_summary(args.summary)
        print('Summary structure valid; evidence still requires source verification')
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')
