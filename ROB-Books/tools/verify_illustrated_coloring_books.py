#!/usr/bin/env python3
"""Validate independently illustrated editions and render all pages for review."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageOps
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/coloring-v2'


def art_sheets():
    out=ROOT/'tmp/coloring-v2/art-review';out.mkdir(parents=True,exist_ok=True)
    report=[]
    for b in json.loads((ROOT/'source/coloring-v2/catalog.json').read_text())['books']:
        files=sorted((ART/b['slug']).glob('[0-9][0-9].png'))
        for start in range(0,len(files),12):
            sheet=Image.new('RGB',(920,1005),'#dedede')
            for j,p in enumerate(files[start:start+12]):
                with Image.open(p) as src:
                    rgb=src.convert('RGB')
                    thumb=ImageOps.contain(rgb,(214,301))
                x=(j%4)*230+8;y=(j//4)*335+7
                sheet.paste(thumb,(x+(214-thumb.width)//2,y))
                ImageDraw.Draw(sheet).text((x,y+309),p.stem+' '+b['pages'][int(p.stem)-1]['title'][:28],fill='black')
            sheet.save(out/f"{b['slug']}-{start//12+1:02d}.jpg",quality=92)
        report.append({'book':b['slug'],'saved':len(files),'expected':len(b['pages'])})
    print(json.dumps(report,indent=2))


def validate(proof=False):
    mp=ROOT/('tmp/pdfs/coloring-v2/proof-manifest.json' if proof else 'source/coloring-v2/publication-manifest.json')
    manifest=json.loads(mp.read_text())
    if not proof: assert len(manifest)==10
    out=ROOT/('tmp/pdfs/coloring-v2/review' if proof else 'output/previews/coloring-v2')
    out.mkdir(parents=True,exist_ok=True)
    all_hashes=set();report=[];cover_pairs={'children':[],'adult':[]}
    for b in manifest:
        path=ROOT/b['file'];doc=fitz.open(path);reader=PdfReader(path)
        expected=30 if b['audience']=='children' else 40
        if not proof:assert b['coloring_pages']==expected
        assert len(doc)==b['coloring_pages']+4==len(reader.pages)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==b['sha256']
        thumbnails=[];min_dpi=999;ink_coverage=[]
        for i,p in enumerate(doc):
            assert tuple(p.rect)==(0,0,612,792),(path,i,'geometry')
            for block in p.get_text('dict')['blocks']:
                if block['type']!=0:continue
                x0,y0,x1,y1=block['bbox']
                assert x0>=30 and x1<=582 and y0>=9 and y1<=760,(path,i,'text outside safe margins',block['bbox'])
            if 2<=i<len(doc)-2:
                record=b['pages'][i-2]
                assert record['title'] in p.get_text(),(path,i,'missing caption')
                assert len(p.get_images())==1,(path,i,'expected one full illustration')
                source=ROOT/record['image']
                sha=hashlib.sha256(source.read_bytes()).hexdigest()
                assert sha==record['sha256']
                assert sha not in all_hashes,(source,'duplicate source used in books')
                all_hashes.add(sha)
                rect=p.get_image_rects(p.get_images()[0][0])[0]
                assert rect.x0>=42.9 and rect.x1<=569.1 and rect.y0>=47.9 and rect.y1<=730.1,(path,i,'image bounds',rect)
                placement=record['placement'];min_dpi=min(min_dpi,placement['effective_dpi'])
                assert placement['effective_dpi']>=145,(source,'low resolution')
                with Image.open(source) as src:
                    pixels=list(src.convert('RGB').resize((256,384)).getdata())
                    colored=sum(max(p)-min(p)>18 for p in pixels)/len(pixels)
                    assert colored<.005,(source,'colored interior')
                    darkness=sum(sum(p)<540 for p in pixels)/len(pixels)
                    assert .015<darkness<.48,(source,'blank or excessively filled page',darkness)
                    ink_coverage.append(float(darkness))
            pix=p.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False)
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            thumb=ImageOps.contain(im,(183,237));tile=Image.new('RGB',(203,263),'#e4e4e4')
            tile.paste(thumb,((203-thumb.width)//2,6))
            ImageDraw.Draw(tile).text((10,245),f'PDF {i+1:02d}',fill='black')
            thumbnails.append(tile)
        category='children' if b['audience']=='children' else 'adult'
        cover_pairs[category].append((thumbnails[0],thumbnails[-1]))
        for start in range(0,len(doc),12):
            sheet=Image.new('RGB',(812,789),'#d4d4d4')
            for j,t in enumerate(thumbnails[start:start+12]):sheet.paste(t,((j%4)*203,(j//4)*263))
            sheet.save(out/f'{path.stem}-sheet-{start//12+1}.jpg',quality=92)
        for i in [0,2,min(16,len(doc)-3),len(doc)-3,len(doc)-1]:
            doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(str(out/f'{path.stem}-page-{i+1:02d}.png'))
        report.append({'file':b['file'],'total_pages':len(doc),'unique_illustrations':b['coloring_pages'],'minimum_effective_dpi':round(min_dpi,1),'mean_ink_coverage':round(sum(ink_coverage)/len(ink_coverage),3),'checks':'page count, unique source art, text, margins, resolution, monochrome, rendering','sha256':b['sha256']})
    for category,pairs in cover_pairs.items():
        if not pairs:continue
        sheet=Image.new('RGB',(203*len(pairs),526),'#d4d4d4')
        for j,(front,back) in enumerate(pairs):
            sheet.paste(front,(203*j,0));sheet.paste(back,(203*j,263))
        sheet.save(out/f'{category}-cover-pairs.jpg',quality=94)
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--proof',action='store_true');ap.add_argument('--art-sheets',action='store_true');a=ap.parse_args()
    if a.art_sheets:art_sheets()
    else:validate(a.proof)
