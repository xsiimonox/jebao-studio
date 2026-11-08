"""Verify the manual archive has the documented Home Assistant layout."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_release', ROOT / 'tools/build_release.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReleaseTests(unittest.TestCase):
    def test_manual_archive_installs_into_custom_components(self):
        config = json.loads((ROOT / 'hacs.json').read_text())
        self.assertNotIn('zip_release', config)
        with tempfile.TemporaryDirectory() as temporary:
            manual = builder.build_release(Path(temporary) / 'dist')
            manual_target = Path(temporary) / 'manual-config'
            with zipfile.ZipFile(manual) as archive:
                self.assertIsNone(archive.testzip())
                archive.extractall(manual_target)
            for relative in ('manifest.json', '__init__.py', 'NOTICE.md', 'panel/jebao-studio.js',
                             'panel/model.js', 'brand/icon.png', 'brand/logo.png', 'translations/de.json'):
                self.assertTrue((manual_target / 'custom_components/jebao_studio' / relative).is_file())
            self.assertEqual(json.loads((manual_target / 'custom_components/jebao_studio' / 'manifest.json').read_text())['domain'], 'jebao_studio')
