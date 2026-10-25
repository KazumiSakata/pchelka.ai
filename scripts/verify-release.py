#!/usr/bin/env python3
"""Verify shipped files and models; no downloads or dependencies."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MANIFEST=ROOT/'RELEASE_MANIFEST.json'
TEXT={'.md','.txt','.json','.py','.js','.mjs','.ts','.tsx','.css','.html','.yaml','.yml','.sh','.bat','.ps1','.toml','.svg','.mts'}
EXCLUDE={'.git','node_modules','__pycache__','.venv','venv','dist','.next','.wrangler','.sites-runtime','backups','uploads','attachments'}
def digest(path):
 data=path.read_bytes()
 if path.suffix in TEXT or path.name in {'.gitignore','.gitattributes','.dockerignore','.npmrc','Dockerfile'}:data=data.replace(b'\r\n',b'\n')
 return hashlib.sha256(data).hexdigest()
def files():
 for p in sorted(ROOT.rglob('*')):
  r=p.relative_to(ROOT)
  if not p.is_file() or any(x in EXCLUDE for x in r.parts) or p.name==MANIFEST.name or p.suffix in {'.pyc','.log','.zip'}:continue
  yield r.as_posix(),p
parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true',help='Maintainer: replace manifest after reviewing changes');a=parser.parse_args()
try:
 if a.write_manifest:
  entries={n:{'bytes':p.stat().st_size,'sha256':digest(p)} for n,p in files()}
  MANIFEST.write_text(json.dumps({'format':1,'hash_policy':'SHA-256; CRLF normalized to LF for text; binary files hashed byte-for-byte','files':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Manifest written:',len(entries),'files');sys.exit(0)
 data=json.loads(MANIFEST.read_text(encoding='utf-8'));errors=[]
 for n,v in data['files'].items():
  p=ROOT/n
  if Path(n).is_absolute() or '..' in Path(n).parts:errors.append('Unsafe manifest path');continue
  if not p.is_file():errors.append('Missing: '+n)
  elif digest(p)!=v['sha256']:errors.append('Changed: '+n)
 vision=json.loads((ROOT/'public/ai/vision-parts.json').read_text())
 if sum((ROOT/'public/ai'/x).stat().st_size for x in vision['parts'])!=vision['size']:errors.append('Vision model size mismatch')
 speech=json.loads((ROOT/'public/speech/model.json').read_text())
 for v in speech['parts']:
  p=ROOT/'public/speech'/v['file']
  if p.stat().st_size!=v['size'] or hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:errors.append('Speech model mismatch: '+v['file'])
 for n,p in files():
  if p.stat().st_size>=100*1024*1024:errors.append('File needs a different Git storage strategy: '+n)
 if errors:print('\n'.join(errors));sys.exit(1)
 print('OK:',len(data['files']),'files; SHA-256, model parts and Git per-file limits verified.')
except (OSError,ValueError,KeyError) as error:print('Verification failed:',error);sys.exit(1)
