"""Deterministic helpers for the Codex research workflow (Python 3.10+)."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from datetime import date

ROOT = Path(__file__).resolve().parents[1]


def read_json(path, empty=False):
    text = Path(path).read_text()
    return {} if empty and not text.strip() else json.loads(text)


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.research-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write('\n')
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_path(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError('Expected repository-relative path')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {relative}')
    return path


def validate(value, schema, label='$'):
    """Validate the JSON Schema subset used by templates/INDEX_template.json.

    Fail closed on unsupported validation keywords so schema changes cannot
    silently weaken validation. This is not a general JSON Schema validator.
    """
    supported = {'$schema', '$id', 'title', 'description', 'type', 'properties',
                 'patternProperties', 'additionalProperties', 'required', 'items',
                 'uniqueItems', 'enum', 'pattern', 'minimum', 'maximum', 'format'}
    unknown = set(schema) - supported
    if unknown:
        raise ValueError(f'{label}: unsupported schema keywords {sorted(unknown)}')
    kinds = {'object': lambda x: isinstance(x, dict),
             'array': lambda x: isinstance(x, list),
             'string': lambda x: isinstance(x, str),
             'integer': lambda x: isinstance(x, int) and not isinstance(x, bool),
             'null': lambda x: x is None}
    expected = schema.get('type', [])
    expected = [expected] if isinstance(expected, str) else expected
    if expected and not any(kinds[t](value) for t in expected):
        raise ValueError(f'{label}: expected {expected}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{label}: invalid enum value')
    if isinstance(value, dict):
        missing = set(schema.get('required', [])) - value.keys()
        if missing:
            raise ValueError(f'{label}: missing {sorted(missing)}')
        for key, item in value.items():
            matches = []
            if key in schema.get('properties', {}):
                matches.append(schema['properties'][key])
            matches.extend(s for p, s in schema.get('patternProperties', {}).items() if re.search(p, key))
            if not matches and schema.get('additionalProperties') is False:
                raise ValueError(f'{label}: unknown field {key}')
            for sub in matches:
                validate(item, sub, f'{label}.{key}')
    elif isinstance(value, list):
        if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            raise ValueError(f'{label}: duplicate items')
        for n, item in enumerate(value):
            validate(item, schema.get('items', {}), f'{label}[{n}]')
    elif isinstance(value, str):
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise ValueError(f'{label}: invalid pattern')
        if schema.get('format') == 'date':
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                raise ValueError(f'{label}: expected ISO date')
            date.fromisoformat(value)
    elif isinstance(value, int):
        if value < schema.get('minimum', value) or value > schema.get('maximum', value):
            raise ValueError(f'{label}: outside range')


def validate_summary(path):
    text = Path(path).read_text()
    for heading in ('Citation', 'Executive Summary', 'Research Problem', 'Methodology',
                    'Experimental Evaluation', 'Contributions', 'Limitations',
                    'Relevance to Our Project', 'Research Opportunities', 'Evidence'):
        if not re.search(r'^##\s+(?:\d+\.\s*)?' + re.escape(heading) + r'\s*$', text, re.M):
            raise ValueError(f'{path}: missing section {heading}')
    if not re.search(r'^source_access:\s*(full_text|abstract_only|unavailable)\s*$', text, re.M):
        raise ValueError(f'{path}: missing source_access metadata')
    evidence = re.split(r'^##\s+(?:\d+\.\s*)?Evidence\s*$', text, flags=re.M)[-1].strip()
    if not evidence or evidence.startswith('- Page/section references for key claims'):
        raise ValueError(f'{path}: evidence section is empty or still a template')


def validate_index(root, index):
    validate(index, read_json(root / 'templates/INDEX_template.json'))
    identifiers = {}
    for paper_id, paper in index.items():
        if not paper['title'].strip() or not paper['authors'] or not paper['url'].startswith(('https://', 'http://')):
            raise ValueError(f'{paper_id}: title, authors and source URL are required')
        doi = paper.get('doi')
        if doi:
            normalized = re.sub(r'^https?://(?:dx\.)?doi.org/', '', doi.lower().strip())
            if normalized in identifiers:
                raise ValueError(f'{paper_id}: duplicate DOI with {identifiers[normalized]}')
            identifiers[normalized] = paper_id
        summary = paper.get('summary_path')
        if summary is not None:
            if summary != f'literature/papers/{paper_id}.md':
                raise ValueError(f'{paper_id}: summary must use stable paper ID')
            path = local_path(root, summary)
            if not path.is_file():
                raise ValueError(f'{paper_id}: missing summary {summary}')
        if paper['status'] == 'analyzed':
            if not summary or not paper.get('date_analyzed'):
                raise ValueError(f'{paper_id}: analyzed paper needs summary and analysis date')
            validate_summary(local_path(root, summary))


def merge_proposal(root, proposal_path, apply=False):
    proposal = read_json(proposal_path)
    if set(proposal) != {'base_sha256', 'updates'} or not isinstance(proposal['updates'], dict):
        raise ValueError('Proposal requires base_sha256 and updates object')
    index_path = root / 'literature/INDEX.json'
    # Only the coordinating Codex agent may call --apply, sequentially.
    if digest(index_path) != proposal['base_sha256']:
        raise ValueError('Stale index proposal; rebase against current index before applying')
    index = read_json(index_path, empty=True)
    merged = copy.deepcopy(index)
    for paper_id, patch in proposal['updates'].items():
        if not isinstance(patch, dict):
            raise ValueError('Each update must be an object')
        merged[paper_id] = {**merged.get(paper_id, {}), **patch}
    validate_index(root, merged)
    if apply:
        if digest(index_path) != proposal['base_sha256']:
            raise ValueError('Index changed during validation')
        atomic_json(index_path, merged)
    return merged
