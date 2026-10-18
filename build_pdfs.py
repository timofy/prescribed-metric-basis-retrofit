"""Typeset the dated manuscript and review report from local sources only."""
from pathlib import Path
import re,json,html,os
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,KeepTogether,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
root=Path(__file__).resolve().parent; out=root/'output';out.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial',str(Path(os.environ.get('WINDIR', 'Windows'))/'Fonts'/ 'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialBold',str(Path(os.environ.get('WINDIR', 'Windows'))/'Fonts'/ 'arialbd.ttf')))
pdfmetrics.registerFont(TTFont('ArialItalic',str(Path(os.environ.get('WINDIR', 'Windows'))/'Fonts'/ 'ariali.ttf')))
pdfmetrics.registerFont(TTFont('MathSymbols',str(Path(os.environ.get('WINDIR', 'Windows'))/'Fonts'/ 'seguisym.ttf')))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='ArialItalic',boldItalic='ArialBold')
navy=HexColor('#183047');gray=HexColor('#52606D');teal=HexColor('#087F80')
styles={
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10,leading=14,spaceAfter=7,textColor=navy),
 'h1':ParagraphStyle('h1',fontName='ArialBold',fontSize=14,leading=18,spaceBefore=13,spaceAfter=8,keepWithNext=True,textColor=navy),
 'h2':ParagraphStyle('h2',fontName='ArialBold',fontSize=11.5,leading=15,spaceBefore=9,spaceAfter=6,keepWithNext=True,textColor=navy),
 'title':ParagraphStyle('title',fontName='ArialBold',fontSize=23,leading=28,spaceAfter=12,textColor=navy),
 'meta':ParagraphStyle('meta',fontName='Arial',fontSize=10,leading=14,spaceAfter=12,textColor=gray),
 'math':ParagraphStyle('math',fontName='Arial',fontSize=11,leading=17,spaceBefore=5,spaceAfter=10,alignment=TA_CENTER,textColor=navy),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=8.3,leading=11,textColor=navy),
 'ref':ParagraphStyle('ref',fontName='Arial',fontSize=9,leading=12,spaceAfter=9,textColor=navy),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=6.8,leading=9,spaceBefore=4,spaceAfter=9,textColor=gray)
}
refs=json.loads((root/'references-final.json').read_text()); numbers={x['key']:i+1 for i,x in enumerate(refs)}
maths=[
 'D<sub>G</sub>(u,v) = {s ∈ V(G) : d<sub>G</sub>(u,s) ≠ d<sub>G</sub>(v,s)}.',
 'β<sub>2</sub>(G) = min {|S| : S ∈ FT(G)},<br/>ρ(G,B) = min {|S| : S ∈ FT(G), B ⊆ S},<br/>p(G,B) = ρ(G,B) − β<sub>2</sub>(G).',
 'E = {01, 02, 03, 14, 25, 45, 56}.',
 '0 ≤ ρ(G,B) − β<sub>2</sub>(G) ≤ 1.',
 'p(G,B) ≤ |B| − L.',
 'd<sub>C</sub>(a,b) + d<sub>C</sub>(b,c) + d<sub>C</sub>(c,a) = d + ℓ = g.',
 '−h, −h + 2, …, h.',
 'h − 1, h − 3, …, −h + 1.',
 'F = {x, y, a<super>*</super>, b<super>*</super>}'
]
def rich(s):
    s=html.escape(s)
    def cite(m):
        parts=m.group(1).split(',',1); k=parts[0]; suffix=(', '+parts[1].strip()) if len(parts)>1 else ''
        return f'<link href="#ref-{numbers[k]}" color="#087F80">[{numbers[k]}{suffix}]</link>'
    s=re.sub(r'\[@([^\]]+)\]',cite,s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);s=re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])',r'<i>\1</i>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Courier" size="8">\1</font>',s)
    s=s.replace('&lt;=','≤').replace('&gt;=','≥')
    s=re.sub(r'\bbeta2\b','β<sub>2</sub>',s);s=re.sub(r'\bbeta\b','β',s);s=re.sub(r'\brho\b','ρ',s)
    for local in ['extension-audit/AUDIT.md','extension-audit/audit-result.json']:
        s=s.replace(local, f'<link href="../{local}" color="#087F80">{local}</link>')
    return s
def footer(c,doc):
    c.saveState();c.setStrokeColor(HexColor('#CCD5DB'));c.line(48,40,547,40)
    c.setFont('Arial',8);c.setFillColor(gray);c.drawString(48,27,'AI-generated draft | Not human peer reviewed | Tim Hughes, project coordinator')
    c.drawRightString(547,27,str(doc.page));c.restoreState()
def build(src,dest,title,manuscript=False):
    s=(root/src).read_text(encoding='utf-8');s=re.sub(r'\A---\n.*?\n---\n','',s,flags=re.S)
    if not manuscript:s=re.sub(r'\A# .*?\n\nTim Hughes.*?\n','',s)
    lines=s.splitlines();story=[Paragraph(title,styles['title']),Paragraph('Tim Hughes - project owner/research coordinator<br/>AI-generated draft; not human peer reviewed',styles['meta'])]
    i=0;mi=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line==r'\[':
            end=lines.index(r'\]',i+1)
            equation=maths[mi]
            for char in '∈⊆≠≤≥ℓ':equation=equation.replace(char,f'<font name="MathSymbols">{char}</font>')
            story.append(Paragraph(equation,styles['math']));mi+=1;i=end+1;continue
        if line.startswith('```'):
            block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            story.append(Preformatted('\n'.join(block),styles['code']));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x) for x in row):rows.append(row)
                i+=1
            cells=[[Paragraph(rich(x),styles['cell']) for x in row] for row in rows]
            n=len(rows[0]); widths=([42,66,78,83,83,147] if n==6 else [65,140,147,147] if n==4 else [90,110,299] if n==3 else [499/n]*n)
            t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#E4EEF0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F5F8F9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.5,gray)]));story.extend([KeepTogether([t,Spacer(1,10)])]);continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));head=line.lstrip('# ').strip()
            if head=='References' and manuscript:
                story.append(Paragraph('References',styles['h1']))
                for j,r in enumerate(refs,1):story.append(Paragraph(f'<a name="ref-{j}"/>[{j}] '+html.escape(r['text'])+f'<br/><link href="{r["url"]}" color="#087F80">{html.escape(r["url"])}</link>',styles['ref']))
                break
            story.append(Paragraph(rich(head),styles['h1' if level==1 else 'h2']));i+=1;continue
        block=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```')) and lines[i].strip()!=r'\[':
            if lines[i].startswith('- '):break
            block.append(lines[i].strip());i+=1
        story.append(Paragraph(rich(' '.join(block)),styles['body']))
    if manuscript:assert mi==len(maths)
    SimpleDocTemplate(str(out/dest),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=46,bottomMargin=57,title=title,author='Tim Hughes (project owner/research coordinator)',pageCompression=1).build(story,onFirstPage=footer,onLaterPages=footer)
build('manuscript.md','paper.pdf','Retaining a metric basis under one sensor erasure in subcubic unicyclic graphs',True)
build('review-report-final.md','review.pdf','Review and limitations report')
print('Built two dated PDFs from local sources only.')
