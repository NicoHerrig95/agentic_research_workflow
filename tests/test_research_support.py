import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from research_support import atomic_json, digest, local_path, merge_proposal, validate, validate_summary
from validate_workspace import check

REPO = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'templates').mkdir()
        (self.root / 'literature').mkdir()
        (self.root / 'templates/INDEX_template.json').write_text((REPO / 'templates/INDEX_template.json').read_text())
        self.paper = dict(title='Verified paper', authors=['Author'], year=None, doi=None,
                          url='https://example.org/paper', topics=[], relevance=dict(score='high', reason='Relevant', related_rqs=[]),
                          contribution='Not assessed', status='discovered', summary_path=None,
                          date_added='2026-10-24', date_analyzed=None)
        atomic_json(self.root / 'literature/INDEX.json', {'P001': self.paper})

    def proposal(self, updates):
        path = self.root / 'proposal.json'
        atomic_json(path, {'base_sha256': digest(self.root / 'literature/INDEX.json'), 'updates': updates})
        return path

    def test_dry_run_then_apply_preserves_unrelated_entries(self):
        proposal = self.proposal({'P002': self.paper})
        original = (self.root / 'literature/INDEX.json').read_bytes()
        merge_proposal(self.root, proposal)
        self.assertEqual(original, (self.root / 'literature/INDEX.json').read_bytes())
        merge_proposal(self.root, proposal, True)
        result = json.loads((self.root / 'literature/INDEX.json').read_text())
        self.assertEqual(result['P001'], self.paper)
        self.assertIn('P002', result)
        with self.assertRaisesRegex(ValueError, 'Stale'):
            merge_proposal(self.root, proposal, True)

    def test_invalid_update_does_not_write(self):
        proposal = self.proposal({'P002': {'title': 'Incomplete'}})
        original = digest(self.root / 'literature/INDEX.json')
        with self.assertRaises(ValueError):
            merge_proposal(self.root, proposal, True)
        self.assertEqual(original, digest(self.root / 'literature/INDEX.json'))

    def test_analyzed_requires_existing_evidence_summary(self):
        proposal = self.proposal({'P001': {'status': 'analyzed', 'summary_path': 'literature/papers/P001.md', 'date_analyzed': '2026-10-24'}})
        with self.assertRaisesRegex(ValueError, 'missing summary'):
            merge_proposal(self.root, proposal)
        papers = self.root / 'literature/papers'
        papers.mkdir()
        summary = (REPO / '.agents/skills/paper_analyst/assets/PAPER_SUMMARY_TEMPLATE.md').read_text()
        (papers / 'P001.md').write_text(summary)
        with self.assertRaisesRegex(ValueError, 'template'):
            merge_proposal(self.root, proposal)
        (papers / 'P001.md').write_text(summary.replace('- Page/section references for key claims', '- Section 2: method definition'))
        merge_proposal(self.root, proposal, True)

    def test_duplicate_doi_rejected(self):
        first = copy.deepcopy(self.paper)
        first['doi'] = '10.1234/example'
        second = {**first, 'doi': 'https://doi.org/10.1234/EXAMPLE'}
        with self.assertRaisesRegex(ValueError, 'duplicate DOI'):
            merge_proposal(self.root, self.proposal({'P001': first, 'P002': second}))

    def test_path_escape_and_unsupported_schema_rejected(self):
        with self.assertRaises(ValueError):
            local_path(self.root, '../outside')
        with self.assertRaises(ValueError):
            validate({}, {'oneOf': []})

    def test_missing_completed_output_rejected(self):
        (self.root / 'PROJECT.md').write_text('Accepted scope')
        state = dict(version=1, stage='analysis', project_sha256=digest(self.root / 'PROJECT.md'),
                     limits=json.loads((REPO / 'workflow/STATE.json').read_text())['limits'],
                     tasks=[dict(id='task1', status='completed', outputs=['missing.md'])], approval_requests=[])
        atomic_json(self.root / 'workflow/STATE.json', state)
        with self.assertRaisesRegex(ValueError, 'Missing task output'):
            check(self.root)


if __name__ == '__main__':
    unittest.main()
