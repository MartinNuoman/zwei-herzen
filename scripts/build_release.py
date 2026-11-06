#!/usr/bin/env python3
"""Rebuild portable exports; exclude private conversation archives and screenshots."""
from pathlib import Path
import json,zipfile
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'content/manifest.json').read_text());notes={}
for chapter in manifest['chapters']:
 cid=chapter['id'];notes[cid]=json.loads((R/f'content/annotations/{cid}.json').read_text())
export={'chapters':notes,'editorial':json.loads((R/'content/learning-editorial.json').read_text())}
(R/'Learning_Notes.json').write_text(json.dumps(export,ensure_ascii=False,indent=2)+'\n')
(R/'Season_01').mkdir(exist_ok=True)
for c in manifest['chapters']:(R/'Season_01'/f'{c["id"]}.txt').write_bytes((R/'content'/c['filename']).read_bytes())
files=[R/n for n in ['index.html','app.js','core.js','styles.css','package.json','README.md','CONTRIBUTING.md','LICENSE-TO-CHOOSE.md','SOURCE_IMPORT_REPORT.md','EDITORIAL_POLICY.md','Zwei_Herzen_Complete.txt','Learning_Notes.json','.gitignore','.nojekyll']]
for folder in ['assets','content','demo','scripts','tests','Season_01']:
 files.extend(p for p in (R/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
with zipfile.ZipFile(R/'GitHub_Release.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,p.relative_to(R))
print(f'Release ready: {len(files)} files; original and site-authored notes labeled separately.')
