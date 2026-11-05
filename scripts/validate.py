#!/usr/bin/env python3
"""Validate local content. Missing declared manuscripts warn; --strict fails on gaps."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[];missing=[]
def read(path):
    try:return path.read_text(encoding='utf-8',errors='strict')
    except (OSError,UnicodeError) as e:errors.append(f'{path.relative_to(ROOT)}: {e}');return ''
def data(path):
    try:return json.loads(read(path))
    except ValueError as e:errors.append(f'{path.relative_to(ROOT)}: invalid JSON: {e}');return {}
def check_annotations(path,text,cid):
    if not path.exists():missing.append(f'annotations: {cid}');return
    d=data(path)
    if d.get('chapterId')!=cid:errors.append(f'{path}: chapterId mismatch')
    ps=[p for p in re.split(r'\n[\t ]*\n',text.replace('\r\n','\n').replace('\r','\n')) if p.strip()]
    spans={}
    for a in d.get('vocabulary',[]):
        p=a.get('paragraph');o=a.get('occurrence');anchor=a.get('anchor')
        if not isinstance(p,int) or p<1 or p>len(ps) or not isinstance(o,int) or o<1 or not isinstance(anchor,str) or not anchor:
            errors.append(f'{path}: invalid annotation anchor/paragraph/occurrence');continue
        matches=list(re.finditer(re.escape(anchor),ps[p-1]))
        if len(matches)<o:errors.append(f'{path}: missing anchor {anchor!r} occurrence {o}');continue
        span=matches[o-1].span()
        if any(span[0]<end and start<span[1] for start,end in spans.get(p,[])):errors.append(f'{path}: overlapping annotations')
        spans.setdefault(p,[]).append(span)
        if not isinstance(a.get('zh'),str) or not a['zh']:errors.append(f'{path}: Chinese gloss required')
    for n in d.get('grammar',[]):
        if not isinstance(n,dict) or not isinstance(n.get('zh'),str):errors.append(f'{path}: grammar note requires zh')
for p in ROOT.rglob('*'):
    if p.is_file() and '.git' not in p.parts and p.suffix in ['.txt','.md','.json','.js','.html','.css','.svg','.py']:read(p)
for p in list((ROOT/'content').rglob('*.json'))+list((ROOT/'demo').glob('*.json')):data(p)
m=data(ROOT/'content/manifest.json');seen=set();orders=set()
chapters=m.get('chapters',[])
expected={f'{i:02}' for i in range(1,13)}|{'epilogue'}
if {c.get('id') for c in chapters}!=expected:errors.append('Season 1 must declare 01–12 and epilogue')
for c in chapters:
    cid=c.get('id')
    if cid in seen:errors.append(f'duplicate ID: {cid}')
    seen.add(cid)
    if c.get('order') in orders:errors.append(f'duplicate order: {c.get("order")}')
    orders.add(c.get('order'))
    if c.get('status') not in ['missing','available']:errors.append(f'{cid}: invalid status')
    p=(ROOT/'content'/c.get('filename','')).resolve()
    if not p.is_relative_to(ROOT/'content/season-01'):errors.append(f'{cid}: filename outside canonical directory');continue
    if not p.is_file():
        missing.append(f'manuscript: {cid}')
        if c.get('status')=='available':errors.append(f'{cid}: marked available but file missing')
    elif c.get('status')!='available':errors.append(f'{cid}: manuscript exists but status is not available')
    if not c.get('title'):missing.append(f'title: {cid}')
    ap=ROOT/'content/annotations'/f'{cid}.json'
    if p.is_file():check_annotations(ap,read(p),cid)
    elif ap.exists():errors.append(f'{cid}: annotations without manuscript')
    else:missing.append(f'annotations: {cid}')
check_annotations(ROOT/'demo/annotations.json',read(ROOT/'demo/chapter.txt'),'demo')
html=read(ROOT/'index.html')
ids=re.findall(r'\bid="([^"]+)"',html)
if len(ids)!=len(set(ids)):errors.append('duplicate HTML IDs')
for link in re.findall(r'(?:src|href)="([^"]+)"',html):
    if link.startswith(('http:','https:','data:')):continue
    if link.startswith('#'):
        if link[1:] not in ids:errors.append(f'broken fragment: {link}')
    elif not (ROOT/link.split('#')[0].split('?')[0]).exists():errors.append(f'broken local link: {link}')
for e in errors:print('ERROR:',e)
for item in missing:print('MISSING:',item)
print(f'{len(errors)} errors; {len(missing)} expected content gaps.')
sys.exit(1 if errors or ('--strict' in sys.argv and missing) else 0)
