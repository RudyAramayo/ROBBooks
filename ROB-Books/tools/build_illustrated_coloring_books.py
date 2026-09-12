#!/usr/bin/env python3
"""Assemble independently illustrated children's and adult ROB coloring books.

No procedural robot illustrations or repeated interior images. The manifest
must have one separately generated illustration for every requested page.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image
from reportlab import rl_config
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'source/coloring-v2/catalog.json'
ART=ROOT/'assets/coloring-v2'
OUT=ROOT/'output/pdf/coloring-v2'
W,H=612,792
# Native binary Flate streams avoid ASCII85 overhead without changing pixels.
rl_config.useA85=0
FONTROOT=Path('/System/Library/Fonts/Supplemental')
FONTS={'Body':'Arial.ttf','BodyBold':'Arial Bold.ttf','Round':'Arial Rounded Bold.ttf','Display':'Georgia Bold.ttf'}
for name,file in FONTS.items():
    p=FONTROOT/file
    if not p.exists(): raise FileNotFoundError(f'Install or supply the font: {p}')
    pdfmetrics.registerFont(TTFont(name,str(p)))

META={
'good-morning-rob':('Good Morning, ROB!',['Good Morning,','ROB!'],'#DD9F28','Wake, wash, tidy, greet.','Cozy rooms, playful shapes, and a garden full of morning discoveries.'),
'rob-counts-the-fireflies':('ROB Counts the Fireflies',['ROB Counts','the Fireflies'],'#7776AE','One little light at a time.','Moonflowers, lily ponds, winding paths, and fireflies to count together.'),
'robs-rainbow-lights':("ROB's Rainbow Lights",["ROB's","Rainbow Lights"],'#229697','A whole world of color.','Lanterns, butterflies, rainy-day puddles, and bright rainbow adventures.'),
'rob-hears-a-little-sound':('ROB Hears a Little Sound',['ROB Hears','a Little Sound'],'#5C936D','Pause. Wonder. Listen.','Raindrops, rustling leaves, bird songs, and quiet moments with friends.'),
'rob-shares-the-shiny-star':('ROB Shares the Shiny Star',['ROB Shares','the Shiny Star'],'#CD795B','One star. Two happy friends.','A shiny discovery becomes a warm adventure in friendship and sharing.'),
'rob-halloween':("ROB's Clockwork Halloween",["ROB's Clockwork","Halloween"],'#C98B49','A season of strange and beautiful things.','Gothic gardens, mechanical ravens, pumpkin lanterns, and moonlit inventions.'),
'rob-thanksgiving':("ROB's Harvest and Thanksgiving",["ROB's Harvest","& Thanksgiving"],'#A97340','Gather the colors of autumn.','Orchards, harvest tables, woven wreaths, and generous moments together.'),
'rob-christmas':("ROB's Christmas Workshop",["ROB's Christmas","Workshop"],'#789B86','Wonder, made one detail at a time.','Snowy villages, clockwork reindeer, festive workshops, and quiet winter rooms.'),
'rob-clockwork-gardens':("ROB's Clockwork Gardens",["ROB's Clockwork","Gardens"],'#6FA7A0','Where mechanics meet the wild.','Orchids, elaborate glasshouses, mechanical pollinators, and impossible gardens.'),
'rob-after-hours':('ROB After Hours: Neon and Smoke',['ROB After Hours','Neon & Smoke'],'#B78DAC','The city has another side.','Anime noir, cannabis smoke, cocktails, music, and adult robot companionship.')
}


def text(c,s,x,y,font='Body',size=12,color=black,align='left'):
    c.setFillColor(color);c.setFont(font,size)
    if align=='center':c.drawCentredString(x,y,s)
    elif align=='right':c.drawRightString(x,y,s)
    else:c.drawString(x,y,s)


def wrapped(c,s,x,y,width,size=12,leading=18,font='Body',color=black,center=False):
    lines=[];line=''
    for word in s.split():
        candidate=(line+' '+word).strip()
        if pdfmetrics.stringWidth(candidate,font,size)>width and line:
            lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    for line in lines:
        text(c,line,x+width/2 if center else x,y,font,size,color,'center' if center else 'left');y-=leading
    return y


def image(c,path,x,y,w,h):
    """Contain the complete illustration; never crop coloring shapes."""
    with Image.open(path) as im:
        iw,ih=im.size
    scale=min(w/iw,h/ih);dw,dh=iw*scale,ih*scale
    c.drawImage(ImageReader(str(path)),x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
    return {'x':x+(w-dw)/2,'y':y+(h-dh)/2,'width':dw,'height':dh,'source_width':iw,'source_height':ih,'effective_dpi':iw/dw*72}


def cover(c,b,back=False,proof=False):
    slug=b['slug'];title,lines,accent,tagline,description=META[slug]
    child=b['audience']=='children';mature=b['audience']=='18plus'
    bg=HexColor('#FFF9EE' if child else '#172C35')
    ink=HexColor('#203E47') if child else HexColor('#FFF8E8')
    ac=HexColor(accent)
    c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ac);c.rect(0,759,W,33,fill=1,stroke=0)
    series="ROB'S LITTLE HELPER COLORING ADVENTURES" if child else 'ROB / ILLUSTRATED COLORING COLLECTION'
    text(c,series,306,770,'BodyBold',9,white,'center')
    if not back:
        font='Round' if child else 'Display'
        for k,line in enumerate(lines):
            size=36
            while pdfmetrics.stringWidth(line,font,size)>520:size-=1
            text(c,line,306,702-k*45,font,size,ink,'center')
        label='30 NEW ILLUSTRATIONS / AGES 3-5' if child else ('40 ILLUSTRATIONS / 18+ ADULT EDITION' if mature else '40 ILLUSTRATIONS / ADULT COLORING')
        text(c,label,306,597,'BodyBold',10,ac,'center')
        c.setFillColor(white);c.roundRect(44,148,524,422,16,fill=1,stroke=0)
        coverart=ART/slug/'cover.png'
        if not coverart.exists():
            if not proof: raise FileNotFoundError(coverart)
            coverart=ART/slug/'01.png'
        image(c,coverart,53,157,506,404)
        text(c,tagline,306,116,'BodyBold',13,ink,'center')
        text(c,'Rodolfo Aramayo and Kierie Aramayo',306,82,'Body',11,ink,'center')
        text(c,'OrbitusRobotics LLC',306,55,'Body',9,ink,'center')
    else:
        heading='A different adventure on every page.' if child else 'Take your time. Make it your own.'
        wrapped(c,heading,63,696,486,25,32,'Round' if child else 'Display',ink,True)
        wrapped(c,description,72,608,468,14,22,'Body',ink,True)
        available=[i for i in [3,12,24] if (ART/slug/f'{i:02d}.png').exists()]
        for k,i in enumerate(available):
            x=49+k*174
            c.setFillColor(white);c.roundRect(x,346,166,214,9,fill=1,stroke=0)
            image(c,ART/slug/f'{i:02d}.png',x+7,353,152,200)
        value='30 distinct scenes, close-ups, and playful shapes.' if child else '40 distinct scenes, still lifes, and ornamental designs.'
        wrapped(c,value,65,303,482,16,23,'BodyBold',ink,True)
        details='Bold outlines and roomy shapes for little artists.' if child else 'Moderate detail, open spaces, and satisfying variety.'
        text(c,details,306,248,'Body',12,ink,'center')
        if mature:
            wrapped(c,'18+ edition. Includes cannabis, tobacco, alcohol, nightlife, and non-explicit adult romance.',80,201,452,11,17,'BodyBold',ac,True)
        else:
            text(c,'Original illustrations created for this coloring edition.',306,194,'Body',10,ink,'center')
        text(c,title,306,122,'BodyBold',13,ink,'center')
        text(c,'OrbitusRobotics LLC',306,82,'BodyBold',11,ink,'center')
        text(c,'Copyright 2026 OrbitusRobotics LLC. All rights reserved.',306,54,'Body',8.5,ink,'center')
    c.showPage()


def intro(c,b):
    slug=b['slug'];child=b['audience']=='children';mature=b['audience']=='18plus'
    text(c,'THIS BOOK BELONGS TO' if child else 'YOUR COLORING ADVENTURE',306,713,'BodyBold',11,align='center')
    c.setLineWidth(1);c.line(110,646,502,646)
    intro='Color, wonder, and explore with ROB.' if child else 'Explore the details. Choose your own palette.'
    text(c,intro,306,588,'Round' if child else 'Display',20,align='center')
    lines=[
        'Each page has its own illustration. Choose any colors you like.',
        'Print on US Letter paper, portrait, at actual size (100%).',
        'For two-sided printing, flip on the long edge.',
        'For markers, print one-sided and use a protective sheet beneath.',
        'Crayons and colored pencils suit two-sided coloring.'
    ]
    if child:lines.insert(0,'Grown-ups can read the short page titles aloud.')
    else:lines.insert(0,'A collection of scenes, close-ups, botanicals, and ornamental designs.')
    y=524
    for line in lines:y=wrapped(c,line,82,y,448,12,20)-15
    if mature:
        wrapped(c,'18+ CONTENT: Cannabis, tobacco, alcohol, nightlife, and non-explicit adult relationships. All characters in this edition are adults.',82,229,448,11,17,'BodyBold')
    else:
        invitation='Look for circles, stars, leaves, and friendly faces as you color.' if child else 'Explore the repeating details, experiment with a palette, and make each scene your own.'
        wrapped(c,invitation,82,219,448,11,17)
    text(c,'Stories and characters: Rodolfo Aramayo and Kierie Aramayo',306,123,'Body',9,align='center')
    text(c,'Original AI-assisted illustrations for this edition, 2026.',306,102,'Body',9,align='center')
    text(c,'OrbitusRobotics LLC',306,80,'BodyBold',10,align='center')
    c.showPage()


def closing(c,b):
    child=b['audience']=='children'
    text(c,'Made with imagination!' if child else 'Your color notes',306,707,'Round' if child else 'Display',28,align='center')
    text(c,'Try your favorite colors here.' if child else 'Keep a few favorite combinations for another day.',306,668,'Body',12,align='center')
    # Palette swatches are supporting paper functionality, not counted as illustrations.
    c.setLineWidth(1.4)
    for row in range(4):
        for col in range(5):c.circle(138+col*84,568-row*94,24,stroke=1,fill=0)
    text(c,META[b['slug']][3],306,139,'BodyBold',14,align='center')
    text(c,'Thank you for coloring with ROB.',306,103,'Body',12,align='center')
    c.showPage()


def build_book(b,proof=False):
    slug=b['slug'];expected=30 if b['audience']=='children' else 40
    assert len(b['pages'])==expected
    missing=[i for i in range(1,expected+1) if not (ART/slug/f'{i:02d}.png').exists()]
    if missing and not proof:raise FileNotFoundError(f'{slug}: missing illustrations {missing}')
    outdir=ROOT/'tmp/pdfs/coloring-v2' if proof else OUT/('children' if b['audience']=='children' else 'adult')
    outdir.mkdir(parents=True,exist_ok=True)
    dest=outdir/f'{slug}-coloring.pdf'
    c=canvas.Canvas(str(dest),pagesize=(W,H),pageCompression=1,invariant=1)
    c.setTitle(META[slug][0]+' - Illustrated Coloring Book')
    c.setAuthor('Rodolfo Aramayo and Kierie Aramayo')
    c.setCreator('OrbitusRobotics LLC / illustrated coloring edition')
    c.setSubject(f'{expected} distinct coloring illustrations; '+b['audience'])
    cover(c,b,proof=proof);intro(c,b)
    pages=[];seen=set()
    for i,p in enumerate(b['pages'],1):
        art=ART/slug/f'{i:02d}.png'
        if not art.exists():continue
        sha=hashlib.sha256(art.read_bytes()).hexdigest()
        assert sha not in seen,(slug,i,'duplicate source image');seen.add(sha)
        placement=image(c,art,43,62,526,682)
        text(c,p['title'],47,39,'Body',9)
        text(c,str(i),565,39,'Body',9,align='right')
        pages.append({'coloring_page':i,'pdf_page':len(pages)+3,'title':p['title'],'image':str(art.relative_to(ROOT)),'sha256':sha,'placement':placement})
        c.showPage()
    closing(c,b);cover(c,b,True,proof);c.save()
    return {'file':str(dest.relative_to(ROOT)),'title':META[slug][0],'audience':b['audience'],'coloring_pages':len(pages),'total_pages':len(pages)+4,'pages':pages,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--proof',action='store_true');ap.add_argument('--book');args=ap.parse_args()
    books=json.loads(CAT.read_text())['books']
    if args.book:books=[b for b in books if b['slug']==args.book]
    assert books,'No matching books'
    manifest=[build_book(b,args.proof) for b in books]
    dest=ROOT/'tmp/pdfs/coloring-v2/proof-manifest.json' if args.proof else ROOT/'source/coloring-v2/publication-manifest.json'
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps([{'file':m['file'],'coloring_pages':m['coloring_pages']} for m in manifest],indent=2))
if __name__=='__main__':main()
