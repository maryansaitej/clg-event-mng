from pathlib import Path
import json,re,collections,logging
import pdfplumber
from pypdf import PdfReader
logging.getLogger('pdfminer').setLevel(logging.ERROR)
D=Path('tmp/pdfs/revision');P=Path('output/pdf/College_Event_Management_Report_Corrected_20_Pages.pdf');m=json.load(open(D/'manifest.json'))
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
with pdfplumber.open(P) as f:
 text=[p.extract_text() or '' for p in f.pages]
 fonts=collections.Counter(c['fontname'] for p in f.pages for c in p.chars)
 sizes=collections.Counter(round(c['size'],2) for p in f.pages for c in p.chars)
 assert len(f.pages)==20
 assert all('TimesNewRoman' in x for x in fonts),fonts
 assert set(sizes)=={12.0,15.0},sizes
 for i,p in enumerate(f.pages,1):
  bad=[c for c in p.chars if c['x0']<70 or c['x1']>542 or c['bottom']>747 or c['top']<20]
  assert not bad,(i,bad[:2])
 for n,y0,y1,t in m['positions']:
  if t in [h for h,p in m['headings']] or t in ['Example Use Case Scenario','Key Framework Features','Architecture Components','1. Frontend Layer','2. Backend Layer','3. Security &amp; Integration','1. Identity and Profile Module','2. Club Module','3. Event Module','4. Registration and Payment Module','5. Dashboard and Administration Module']:
   chars=[c for c in f.pages[n-1].chars if c['top']>=792-y0-1 and c['bottom']<=792-y1+1]
   assert chars and all(round(c['size'],1)==15 for c in chars),('Heading size',n,t)
for h,n in m['headings']:
 assert norm(h) in norm(text[n-1]),(h,n)
 if n>=8:assert norm(h) in norm(text[2]+text[3]),('TOC omission',h)
required=[f'1.{i}' for i in range(1,5)]+[f'2.{i}' for i in range(1,7)]+[f'3.{i}' for i in range(1,8)]+[f'4.{i}' for i in range(1,5)]
for key in required:assert any(h.startswith(key+' ') for h,n in m['headings']),key
for title,n in m['figures']:assert norm(title) in norm(text[n-1]) and norm(title) in norm(text[4])
for title,n in m['tables']:assert norm(title) in norm(text[n-1]) and norm(title) in norm(text[5])
for forbidden in ['4.5 Data Flow Model','4.6 Working of the Proposed System','4.7 Key Features','4.8 Advantages','5. Methodology','5.6 Code','5.7 Testing','6. Conclusion','7. Key Outcomes','8. Future Enhancements','References','LOGIN AND REGISTER PAGES','Entity-relationship model']:
 assert not any(norm(forbidden)==norm(line) or (forbidden!='References' and norm(forbidden) in norm(line)) for x in text for line in x.splitlines()),forbidden
r=PdfReader(P);assert r.page_labels==['i','ii','iii','iv','v','vi','vii']+[str(i) for i in range(1,14)]
result={'pages':20,'required_numbered_subsections':len(required),'last_section':'4.4 Key System Components','all_rendered_fonts':dict(fonts),'all_rendered_sizes':dict(sizes),'contents_and_captions':'verified','text_bounds':'verified','later_template_sections':'absent','frontend_and_backend':'covered in sections 1.4, 4.2, 4.3 and 4.4','file_bytes':P.stat().st_size}
print(json.dumps(result,indent=2));json.dump(result,open(D/'verification.json','w'),indent=2)
