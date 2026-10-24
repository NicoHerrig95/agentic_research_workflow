"""Validate research artifacts and resumable workflow references."""
import argparse
from research_support import ROOT, digest, local_path, read_json, validate_index
from workflow_state import STAGES
from workflow_config import load_config, paper_capacity


def check(root):
    warnings = []
    validate_index(root, read_json(root / 'literature/INDEX.json', empty=True))
    state = read_json(root / 'workflow/STATE.json')
    if state.get('version') != 1 or state.get('stage') not in STAGES:
        raise ValueError('Invalid workflow version or stage')
    if not isinstance(state.get('tasks'), list) or not isinstance(state.get('approval_requests'), list):
        raise ValueError('State requires tasks and approval_requests lists')
    required_limits = ('max_search_queries', 'max_candidates', 'max_papers',
                       'max_parallel_analysts', 'max_cycles', 'max_task_attempts')
    limits = state.get('limits', {})
    for name in required_limits:
        if type(limits.get(name)) is not int or limits[name] < 1:
            raise ValueError(f'Invalid workflow limit: {name}')
    config = load_config(root)
    paper_capacity(state, config)
    if config["obsidian_vault"] is None:
        warnings.append("OBSIDIAN_VAULT is not configured in .env; set it before syncing")
    ids = set()
    for task in state['tasks']:
        if not isinstance(task, dict) or not isinstance(task.get('id'), str) or task['id'] in ids:
            raise ValueError('Invalid or duplicate task ID')
        ids.add(task['id'])
        if task.get('status') not in ('pending', 'running', 'completed', 'failed', 'blocked'):
            raise ValueError(f"Invalid task status: {task['id']}")
        if task.get('status') == 'completed' and not task.get('outputs'):
            raise ValueError(f"Completed task has no outputs: {task['id']}")
        for output in task.get('outputs', []):
            if not local_path(root, output).is_file():
                raise ValueError(f'Missing task output: {output}')
    for request in state['approval_requests']:
        if request.get('status') not in ('pending', 'approved', 'rejected'):
            raise ValueError('Invalid approval status')
        if not local_path(root, request['proposal_path']).is_file():
            raise ValueError('Missing approval proposal')
        if request['status'] == 'approved' and not request.get('user_decision_reference'):
            raise ValueError('Approved proposal needs a user decision reference')
    if state.get('project_sha256') != digest(root / 'PROJECT.md'):
        warnings.append('Project differs from checkpoint; reassess task relevance before resuming')
    if not (root / 'RESEARCH_PROPOSAL.md').is_file():
        warnings.append('RESEARCH_PROPOSAL.md is missing; research intake cannot proceed')
    if '- Working title' in (root / 'PROJECT.md').read_text():
        warnings.append('PROJECT.md still contains the initial scope template')
    return warnings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        for warning in check(ROOT):
            print(f'Warning: {warning}')
        print('Workspace structure valid (scientific correctness is not checked)')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Error: {exc}\n')
