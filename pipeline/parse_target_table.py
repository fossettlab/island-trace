#!/usr/bin/env python3
"""Best-effort structuring of the OCR'd target table (columns printed on the sheet: "No.", "E", "N",
"Ht", "Axis").  For every grid reference we take the next two OCR tokens: a 1-2 digit number <= 25 is
read as Ht (height, metres), a 2-3 digit number <= 360 as Axis (bearing, degrees), and "conc"
(or the OCR garbles oono/aono/cono/cone) as "concentration".  Everything is kept verbatim as well.
writes: data/derived/target_table.csv
"""
import csv, re
rows = list(csv.DictReader(open('data/derived/ocr_points_wgs84.csv')))
out = []
for r in rows:
    toks = r['following_tokens'].split(' | ')
    ht = axis = conc = ''
    for t in toks[:2]:
        if re.fullmatch(r'\d{1,2}', t) and int(t) <= 25 and not ht: ht = int(t)
        elif re.fullmatch(r'\d{2,3}', t) and int(t) <= 360 and not axis: axis = int(t)
        elif re.fullmatch(r'[oacc]?[oc]n[oce]', t) or t == 'conc': conc = 'conc'
    series = ('1200' if re.fullmatch(r'12\d\d', r['ocr_id']) else '300' if re.fullmatch(r'3\d\d', r['ocr_id'])
              else '400/1400' if re.fullmatch(r'(4\d\d|14\d\d|T14\d\d|4\.68|U,149)', r['ocr_id']) else 'other')
    out.append(dict(ocr_id=r['ocr_id'], series=series, grid_E4=r['grid_E4'], grid_N4=r['grid_N4'],
                    lon=r['lon'], lat=r['lat'], Ht=ht, Axis=axis, conc=conc, raw_following=r['following_tokens']))
with open('data/derived/target_table.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
from collections import Counter
print(Counter(o['series'] for o in out)); print(sum(1 for o in out if o['Ht']!=''), 'Ht values;', sum(1 for o in out if o['Axis']!=''), 'Axis values;', sum(1 for o in out if o['conc']), 'conc')
