import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ROOT / 'skills/george-orchestrate/adapters'
FROZEN = {
    'codex.md': 'da7839d762fa734ab1e84b58f1a0c5a85a763649b5324720840fc1e905ad5c70',
    'cursor.md': 'a2044be56939cd165fef700624efe81db8740efdd54de236c1d1d164c91473a0',
    'omp.md': 'ef1d1fb9c1e9cf71a6d0256a7d184c7e137378bc4b93f474da7de62a781d6493',
}


class GrokAdapterIsolationTests(unittest.TestCase):
    def test_existing_adapters_unchanged(self):
        for name, digest in FROZEN.items():
            path = ADAPTERS / name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, name)

    def test_grok_adapter_exists_and_is_grok_native(self):
        text = (ADAPTERS / 'grok.md').read_text()
        self.assertIn('spawn_subagent', text)
        self.assertIn('0.3.4', text)
        self.assertIn('Do not modify `adapters/codex.md`', text)
        self.assertIn('Never open `codex.md`', text)
        self.assertIn('general-purpose', text)
        self.assertIn('explore', text)
        self.assertIn('resume_from', text)
        self.assertIn('depth limit', text)

    def test_shared_entries_route_to_grok_without_install_host(self):
        skill = (ROOT / 'skills/george-mode/SKILL.md').read_text()
        orch = (ROOT / 'skills/george-orchestrate/SKILL.md').read_text()
        hosts = (ROOT / 'skills/george-mode/references/hosts.md').read_text()
        install = (ROOT / 'scripts/install.py').read_text()
        self.assertIn('adapters/grok.md', skill)
        self.assertIn('adapters/grok.md', orch)
        self.assertIn('Grok CLI', hosts)
        self.assertIn("home / '.agents/skills'", install)
        self.assertNotIn('.grok/skills', install)

    def test_capability_schema_keeps_empty_catalogs(self):
        schema = json.loads((ADAPTERS / 'grok-capability.schema.json').read_text())
        self.assertEqual(schema['properties']['models']['default'], [])
        self.assertEqual(schema['properties']['types']['default'], [])
        self.assertEqual(schema['properties']['tool']['properties']['name']['const'], 'spawn_subagent')
        self.assertEqual(schema['properties']['depth']['properties']['max_nesting']['const'], 1)


if __name__ == '__main__':
    unittest.main()
