from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from workflow_config import load_config, paper_capacity


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_defaults_and_literal_values(self):
        self.assertEqual(load_config(self.root)['max_parallel_papers'], 3)
        (self.root / '.env').write_text('OBSIDIAN_VAULT = "My Research Vault"\nMAX_PARALLEL_PAPERS=1 # sequential\nUNRELATED_SECRET=hidden\n')
        self.assertEqual(load_config(self.root), {'obsidian_vault': 'My Research Vault', 'max_parallel_papers': 1})

    def test_invalid_limits_fail_closed(self):
        for value in ('0', '-1', '1.5', 'many', '', '$(echo 3)'):
            with self.subTest(value=value):
                (self.root / '.env').write_text(f'MAX_PARALLEL_PAPERS={value}\n')
                with self.assertRaises(ValueError):
                    load_config(self.root)

    def test_duplicate_and_broken_quote_rejected(self):
        for text in ('MAX_PARALLEL_PAPERS=2\nMAX_PARALLEL_PAPERS=3', 'OBSIDIAN_VAULT="broken'):
            (self.root / '.env').write_text(text)
            with self.assertRaises(ValueError):
                load_config(self.root)

    def test_ceiling_and_slots(self):
        state = {'limits': {'max_parallel_analysts': 3}, 'tasks': [
            {'role': 'paper_analyst', 'status': 'running'},
            {'role': 'paper_analyst', 'status': 'completed'},
            {'role': 'literature_scout', 'status': 'running'}]}
        config = {'max_parallel_papers': 2}
        self.assertEqual(paper_capacity(state, config), {'effective_max_parallel_papers': 2, 'running': 1, 'available_slots': 1})
        state['limits']['max_parallel_analysts'] = 1
        self.assertEqual(paper_capacity(state, config)['available_slots'], 0)
        state['tasks'].append({'role': 'paper_analyst', 'status': 'running'})
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            paper_capacity(state, config)


if __name__ == '__main__':
    unittest.main()
