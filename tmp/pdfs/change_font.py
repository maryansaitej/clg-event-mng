from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import DictionaryObject,NameObject,NumberObject,FloatObject,ArrayObject,DecodedStreamObject
from pypdf._cmap import get_encoding
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase._glyphlist import _glyphname2unicode
from reportlab.pdfbase.pdfmetrics import stringWidth
P=Path('output/pdf/College_Event_Management_Project_Report.pdf');r=PdfReader(P);w=PdfWriter();w.clone_document_from_reader(r)
N=NameObject
cache={};seen=set();count=0

def embed(style):
 if style in cache:return cache[style]
 suffix={'regular':'','bold':' Bold','italic':' Italic'}[style]
 path=Path('/System/Library/Fonts/Supplemental/Times New Roman'+suffix+'.ttf');tt=TTFont('TNR'+style,str(path)).face;scale=1
 name='TimesNewRomanPS'+{'regular':'MT','bold':'-BoldMT','italic':'-ItalicMT'}[style]
 stream=DecodedStreamObject();raw=path.read_bytes();stream.set_data(raw);stream[N('/Length1')]=NumberObject(len(raw));file=w._add_object(stream.flate_encode())
 d=DictionaryObject({N('/Type'):N('/FontDescriptor'),N('/FontName'):N('/'+name),N('/Flags'):NumberObject(32+(64 if style=='italic' else 0)),N('/FontBBox'):ArrayObject([FloatObject(v*scale) for v in tt.bbox]),N('/ItalicAngle'):FloatObject(tt.italicAngle),N('/Ascent'):FloatObject(tt.ascent*scale),N('/Descent'):FloatObject(tt.descent*scale),N('/CapHeight'):FloatObject(700),N('/StemV'):NumberObject(120 if style=='bold' else 80),N('/FontFile2'):file})
 cache[style]=(name,w._add_object(d),{u:min([n for n,v in _glyphname2unicode.items() if v==u],key=len,default='uni%04X'%u) for u in tt.charToGlyph});return cache[style]
def resources(res):
 global count
 if '/Font' in res:
  for key,ref in list(res['/Font'].items()):
   f=ref.get_object();ident=id(f)
   if ident in seen:continue
   seen.add(ident);oldname=str(f.get('/BaseFont',''))
   style='bold' if 'Bold' in oldname or (f.get('/Subtype')=='/Type3' and key=='/F4') else 'italic' if 'Italic' in oldname else 'regular'
   name,desc,cmap=embed(style);enc,mp=get_encoding(f)
   def char(code):
    v=enc.get(code,chr(code)) if isinstance(enc,dict) else bytes([code]).decode(enc,errors='replace')
    return mp.get(v,v)
   chars=[char(i) for i in range(256)]
   dif=ArrayObject([NumberObject(0)]+[N('/'+cmap.get(ord(t),'.notdef')) if len(t)==1 else N('/.notdef') for t in chars])
   if '/Widths' in f:
    first=int(f.get('/FirstChar',0));last=int(f.get('/LastChar',255));scale=float(f['/FontMatrix'][0])*1000 if f.get('/Subtype')=='/Type3' else 1
    widths=ArrayObject([FloatObject(float(v)*scale) for v in f['/Widths']])
   else:
    first=0;last=255;widths=ArrayObject([FloatObject(stringWidth(t,oldname.lstrip('/') or 'Helvetica',1000)) if len(t)==1 else NumberObject(0) for t in chars])
   uni=f.get('/ToUnicode')
   if uni is None:
    lines=['/CIDInit /ProcSet findresource begin','12 dict begin','begincmap','/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def','/CMapName /TNRUnicode def','/CMapType 2 def','1 begincodespacerange','<00> <FF>','endcodespacerange']
    valid=[(i,t) for i,t in enumerate(chars) if len(t)==1]
    for start in range(0,len(valid),100):
     part=valid[start:start+100];lines += [f'{len(part)} beginbfchar']+[f'<{i:02X}> <{t.encode("utf-16-be").hex()}>' for i,t in part]+['endbfchar']
    lines+=['endcmap','CMapName currentdict /CMap defineresource pop','end','end'];s=DecodedStreamObject();s.set_data('\n'.join(lines).encode());uni=w._add_object(s)
   f.clear();f.update({N('/Type'):N('/Font'),N('/Subtype'):N('/TrueType'),N('/BaseFont'):N('/'+name),N('/FirstChar'):NumberObject(first),N('/LastChar'):NumberObject(last),N('/Widths'):widths,N('/FontDescriptor'):desc,N('/Encoding'):DictionaryObject({N('/Type'):N('/Encoding'),N('/Differences'):dif}),N('/ToUnicode'):uni});count+=1
 for ref in res.get('/XObject',{}).values():
  obj=ref.get_object()
  if '/Resources' in obj:resources(obj['/Resources'])
for page in w.pages:resources(page['/Resources'])
out=P.with_name(P.stem+'_Times_New_Roman.pdf')
with out.open('wb') as f:w.write(f)
check=PdfReader(out);assert len(check.pages)==30
for i,(a,b) in enumerate(zip(r.pages,check.pages)):
 assert ''.join(a.extract_text().split())==''.join(b.extract_text().split()),('Text changed',i+1)
print(out,'fonts replaced:',count,'pages:',len(check.pages),'all text preserved')
