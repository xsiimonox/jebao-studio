"""Build the manual-install ZIP rooted at custom_components/."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / 'custom_components/jebao_studio'

def build_release(output_dir=None):
    version = json.loads((INTEGRATION / 'manifest.json').read_text())['version']
    output_dir = Path(output_dir) if output_dir is not None else ROOT / 'dist'
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f'jebao-studio-{version}.zip'
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(INTEGRATION.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                archive.write(path, path.relative_to(ROOT))
        archive.write(ROOT / 'NOTICE.md', 'custom_components/jebao_studio/NOTICE.md')
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert 'custom_components/jebao_studio/manifest.json' in archive.namelist()
    return output


if __name__ == '__main__':
    print(build_release())
