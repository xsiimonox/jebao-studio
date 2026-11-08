"""Build separate archives for HACS and manual installation."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / 'custom_components/jebao_studio'

def build_release(output_dir=None):
    version = json.loads((INTEGRATION / 'manifest.json').read_text())['version']
    output_dir = Path(output_dir) if output_dir is not None else ROOT / 'dist'
    output_dir.mkdir(parents=True, exist_ok=True)
    manual = output_dir / f'jebao-studio-{version}.zip'
    hacs = output_dir / 'jebao_studio.zip'
    for output, base in ((manual, ROOT), (hacs, INTEGRATION)):
        # HACS extracts straight into /config/custom_components/jebao_studio/.
        # A ZIP with a custom_components/ prefix would install one level too deep.
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(INTEGRATION.rglob('*')):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                    archive.write(path, path.relative_to(base))
            prefix = 'custom_components/jebao_studio/' if output == manual else ''
            archive.write(ROOT / 'NOTICE.md', prefix + 'NOTICE.md')
        with zipfile.ZipFile(output) as archive:
            assert archive.testzip() is None
            assert prefix + 'manifest.json' in archive.namelist()
    return manual, hacs


if __name__ == '__main__':
    for output in build_release():
        print(output)
