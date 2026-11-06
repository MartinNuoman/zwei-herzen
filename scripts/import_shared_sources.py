#!/usr/bin/env python3
"""Reproduce canonical text from locally archived, rendered share-page blocks.
The archive is private working evidence and is deliberately excluded from publication.
"""
from pathlib import Path
import json,re,hashlib,zipfile
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
def save(p,d):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sources={i:load(f'source-archive/source-{i}.json') for i in (1,2,3)}
cards={i:load(f'source-archive/source-{i}-cards.json') for i in (1,2)}
# Explicit audited narrative boundaries; chapter previews and study UI are excluded.
specs=[('01',2,3,4,32,32,51),('02',2,4,4,100,100,134),('03',2,5,3,160,160,205),('04',2,7,38,186,186,191),('05',2,9,4,185,185,218),('06',2,10,4,184,184,231),('07',1,0,6,78,79,95),('08',1,1,4,125,125,143),('09',3,0,7,179,179,198),('10',3,2,7,194,194,208),('11',3,6,8,258,258,273),('12',3,14,12,366,405,418),('epilogue',3,14,367,404,405,418)]
titles={'09':'Eine kleine Überraschung','10':'Unser erstes Zuhause','11':'Besuch von den Eltern','epilogue':'Epilog'}
manifest=load('content/manifest.json');formats={};provenance=[];allnotes={};complete=[]
for cid,s,sec,start,end,ns,ne in specs:
 section=sources[s]['sections'][sec];blocks=section['blocks'];selected=[(j,b) for j,b in enumerate(blocks[start:end],start) if b['text'].strip() and not b['text'].startswith(('Fortsetzung folgt','Ende von Kapitel'))]
 paragraphs=[b['text'] for j,b in selected]
 # One UTF-8 canonical paragraph per source paragraph/heading/blockquote; no prose rewriting.
 text='\n\n'.join(paragraphs)+'\n';(R/f'content/season-01/{cid}.txt').write_text(text)
 formats[cid]=[{'paragraph':i+1,'kind':'heading' if b['tag'].startswith('H') else 'quote' if b['tag']=='BLOCKQUOTE' else 'paragraph','italic':b['runs']} for i,(j,b) in enumerate(selected)]
 notes=blocks[ns:ne];glossary=[]
 if s in cards:
  for c in cards[s][sec]['cards']:
   if not c['parts']:continue
   lines=[line.strip() for line in c['text'].splitlines() if line.strip()]
   term=c['parts'][0]
   # Card body only; no definitions are supplied for collapsed/inaccessible cards.
   zh=next((x for x in lines[1:] if re.search('[\u4e00-\u9fff]',x) and '点击查看' not in x),None)
   item={'term':term,'sourceText':c['text']}
   if zh:item['zh']=zh
   if len(c['parts'])>=3:item['example']=c['parts'][2]
   glossary.append(item)
 for b in notes:
  if b['tag']=='TABLE':
   rows=b['rows'];head=rows[0]
   for row in rows[1:]:
    if len(row)<2:continue
    item={'term':row[0]}
    if len(row)==2:item['zh']=row[1]
    elif 'English' in head[1]:item.update(en=row[1],zh=row[2])
    else:item.update(zh=row[1],note=row[2])
    glossary.append(item)
 # Preserve the original learning section as readable plain text as well as structured terms.
 original_notes=[]
 for b in notes:
  if b['tag']=='TABLE':original_notes.append('\n'.join(' | '.join(row) for row in b['rows']))
  else:original_notes.append(b['display'] or b['text'])
 grammar=[{'zh':'\n\n'.join(original_notes)}] if original_notes else []
 # Card spans (e.g. grammar notes) are not always paragraph elements: retain their exact text.
 for item in glossary:
  if item.get('sourceText') and item['sourceText'] not in grammar[0]['zh']:
   grammar[0]['zh']+='\n\n'+item['sourceText']
 vocabulary=[];unanchored=[];occupied={}
 for item in glossary:
  if not item.get('zh'):unanchored.append({'term':item['term'],'reason':'Definition not exposed in supplied shared page'});continue
  term=item['term'];candidates=[term,re.sub(r'^(?:der|die|das|sich)\s+','',term).split(' + ')[0]]
  found=None
  for candidate in candidates:
   if not candidate:continue
   for pi,p in enumerate(paragraphs,1):
    m=re.search(re.escape(candidate),p,re.I)
    if m:found=(pi,m);break
   if found:break
  if not found:
   base=candidates[-1];base=re.sub(r'(?:en|ern)$','',base)
   if len(base)>=4 and ' ' not in base:
    for pi,p in enumerate(paragraphs,1):
     m=re.search(r'(?<!\w)'+re.escape(base)+r'\w*',p,re.I)
     if m:found=(pi,m);break
  if not found:unanchored.append({'term':term,'reason':'Supplied lemma or phrase has no exact story anchor; retained in glossary'});continue
  pi,m=found;span=m.span()
  if any(span[0]<b and a<span[1] for a,b in occupied.get(pi,[])):continue
  occupied.setdefault(pi,[]).append(span)
  anchor=m.group();occ=len(list(re.finditer(re.escape(anchor),paragraphs[pi-1][:m.end()])))
  entry={'paragraph':pi,'anchor':anchor,'occurrence':occ,'zh':item['zh'],'term':term}
  for k in ['en','example','note']:
   if k in item:entry[k]=item[k]
  vocabulary.append(entry)
 annotation={'chapterId':cid,'source':sources[s]['url'],'vocabulary':vocabulary,'grammar':grammar,'glossary':glossary,'unanchored':unanchored}
 save(f'content/annotations/{cid}.json',annotation);allnotes[cid]=annotation
 c=next(c for c in manifest['chapters'] if c['id']==cid);c['status']='available';c['title']=titles.get(cid,c['title']);c['source']=sources[s]['url']
 provenance.append({'chapterId':cid,'source':sources[s]['url'],'sectionIndex':sec,'sourceBlockIndices':[j for j,b in selected],'sha256':hashlib.sha256(text.encode()).hexdigest(),'paragraphCount':len(paragraphs)})
 complete.append((f'Kapitel {int(cid)} — ' if cid!='epilogue' else '')+c['title']+'\n\n'+text)
# Original follow-up explanations, kept verbatim and separate from manuscript.
for cid,source_id,indices in [('04',2,[8]),('06',2,[11,12]),('08',1,[2]),('10',3,[1,3]),('11',3,[7,8]),('12',3,[15,16,17,18])]:
 annotation=allnotes[cid]
 annotation['supplementary']=[{'source':sources[source_id]['url'],'text':sources[source_id]['sections'][i]['text']} for i in indices]
 annotation['grammar'].extend({'zh':item['text']} for item in annotation['supplementary'])
 save(f'content/annotations/{cid}.json',annotation)
save('content/manifest.json',manifest);save('content/formatting.json',formats);save('content/provenance.json',{'method':'Rendered source paragraphs, unchanged wording; story separated from learning notes, image search widgets, introductions and previews. No continuity edits.','chapters':provenance});save('Learning_Notes.json',{'chapters':allnotes,'editorial':load('content/learning-editorial.json') if (R/'content/learning-editorial.json').exists() else None})
(R/'Zwei_Herzen_Complete.txt').write_text('Zwei Herzen, ein Zuhause\nStaffel 1\n\n'+'\n\n'.join(complete))
(R/'Season_01').mkdir(exist_ok=True)
for p in (R/'content/season-01').glob('*.txt'):(R/'Season_01'/p.name).write_bytes(p.read_bytes())
print('Imported 12 chapters + epilogue; annotations:',sum(len(a['vocabulary']) for a in allnotes.values()))
