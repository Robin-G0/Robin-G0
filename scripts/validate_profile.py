"""Reject invalid generated profile files before they can be published."""

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def validate_outputs(outputs):
    for filename, content in outputs.items():
        if re.search(r'^(?:<{7}|={7}|>{7})(?:\s|$)', content, re.M):
            raise ValueError(f'Unresolved merge conflict in {filename}')
        if filename.endswith('.svg'):
            root = ET.fromstring(content)
            if root.tag != '{http://www.w3.org/2000/svg}svg':
                raise ValueError(f'Invalid SVG root in {filename}')
        elif filename.endswith('.json'):
            json.loads(content)


def main():
    root = Path(__file__).resolve().parents[1]
    paths = [root / 'README.md', *sorted((root / 'assets').rglob('*')),
             *sorted((root / 'themes').rglob('*'))]
    outputs = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8')
               for p in paths if p.is_file() and p.suffix in ('.md', '.json', '.svg')}
    validate_outputs(outputs)
    print(f'Validated {len(outputs)} profile files: no merge markers, valid SVG and JSON.')


if __name__ == '__main__':
    main()
