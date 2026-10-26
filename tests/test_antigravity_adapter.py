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
    'grok.md': 'ebc43008b96ec18909c5b0ca3defcfd17bbcea9ae92a90e27b81b36e31a6bb7c',
}


class AntigravityAdapterIsolationTests(unittest.TestCase):
    def test_existing_four_adapters_unchanged(self):
        for name, digest in FROZEN.items():
            path = ADAPTERS / name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, name)

    def test_antigravity_adapter_exists_and_is_antigravity_native(self):
        text = (ADAPTERS / 'antigravity.md').read_text()
        self.assertIn('invoke_subagent', text)
        self.assertIn('define_subagent', text)
        self.assertIn('send_message', text)
        self.assertIn('manage_subagents', text)
        self.assertIn('0.3.5', text)
        self.assertIn('Do not modify `adapters/codex.md`', text)
        self.assertIn('Never open `codex.md`', text)
        self.assertIn('TypeName: "self"', text)
        self.assertIn('TypeName: "research"', text)
        self.assertIn('Reactive wakeup', text)

    def test_shared_entries_route_to_antigravity_and_install_gemini_config_skills(self):
        skill = (ROOT / 'skills/george-mode/SKILL.md').read_text()
        orch = (ROOT / 'skills/george-orchestrate/SKILL.md').read_text()
        hosts = (ROOT / 'skills/george-mode/references/hosts.md').read_text()
        install = (ROOT / 'scripts/install.py').read_text()
        linkcheck = (ROOT / 'scripts/linkcheck.py').read_text()
        self.assertIn('adapters/antigravity.md', skill)
        self.assertIn('adapters/antigravity.md', orch)
        self.assertIn('Antigravity', hosts)
        self.assertIn("home / '.gemini/config/skills'", install)
        self.assertIn("Path.home() / '.gemini/config/skills'", linkcheck)

    def test_capability_schema_keeps_empty_catalogs(self):
        schema = json.loads((ADAPTERS / 'antigravity-capability.schema.json').read_text())
        self.assertEqual(schema['properties']['models']['default'], [])
        self.assertEqual(schema['properties']['types']['default'], [])
        self.assertEqual(schema['properties']['tool']['properties']['name']['const'], 'invoke_subagent')
        self.assertEqual(schema['properties']['tool']['properties']['follow_up']['const'], 'send_message')
        self.assertEqual(schema['properties']['tool']['properties']['manage']['const'], 'manage_subagents')
        self.assertEqual(schema['properties']['depth']['properties']['max_nesting']['const'], 1)


if __name__ == '__main__':
    unittest.main()
