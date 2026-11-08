"""Verify HACS archive extraction uses the real integration installation root."""
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
    def test_hacs_and_manual_archives_install_identical_content(self):
        config = json.loads((ROOT / 'hacs.json').read_text())
        self.assertTrue(config['zip_release'])
        with tempfile.TemporaryDirectory() as temporary:
            manual, hacs = builder.build_release(Path(temporary) / 'dist')
            self.assertEqual(hacs.name, config['filename'])
            hacs_target = Path(temporary) / 'hacs-config/custom_components/jebao_studio'
            manual_target = Path(temporary) / 'manual-config'
            with zipfile.ZipFile(hacs) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('manifest.json', archive.namelist())
                self.assertFalse(any(name.startswith('custom_components/') for name in archive.namelist()))
                archive.extractall(hacs_target)
            with zipfile.ZipFile(manual) as archive:
                self.assertIsNone(archive.testzip())
                archive.extractall(manual_target)
            for relative in ('manifest.json', '__init__.py', 'NOTICE.md', 'panel/jebao-studio.js',
                             'panel/model.js', 'brand/icon.png', 'brand/logo.png', 'translations/de.json'):
                self.assertEqual((hacs_target / relative).read_bytes(),
                    (manual_target / 'custom_components/jebao_studio' / relative).read_bytes())
            self.assertEqual(json.loads((hacs_target / 'manifest.json').read_text())['domain'], 'jebao_studio')
