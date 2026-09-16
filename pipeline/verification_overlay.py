#!/usr/bin/env python3
"""Draw the table's coordinates, modern rivers and landmark positions on the scan through the fitted transform."""
import sys, csv, numpy as np, cv2, rasterio, pyarrow.parquet as pq
from shapely import wkb
from pyproj import Transformer
scan, table, out = sys.argv[1:4]
base = scan.rsplit('.', 1)[0]
with rasterio.open(base + '_georef.tif') as d: inv = ~d.transform
im = cv2.imread(scan); tr = Transformer.from_crs('EPSG:4326', 'EPSG:27500', always_xy=True)
for r in pq.read_table('data/derived/overture_water.parquet').to_pylist():
    if r['subtype'] not in ('river', 'canal'): continue
    g = wkb.loads(r['geometry'])
    for p in (g.geoms if g.geom_type.startswith('Multi') else [g]):
        coords = p.exterior.coords if p.geom_type == 'Polygon' else p.coords
        pts = np.array([inv * tr.transform(x, y) for x, y in coords], dtype=np.int32).reshape(-1, 1, 2)
        cv2.polylines(im, [pts], p.geom_type == 'Polygon', (255, 120, 0), 1)
for p in csv.DictReader(open(table)):
    x, y = inv * (300000 + int(p['grid_E4'])*10, 500000 + int(p['grid_N4'])*10)
    cv2.circle(im, (int(x), int(y)), 9, (0, 180, 0), 2)
for name, lon, lat in [('Elst church', 5.8590, 51.9190), ('Huissen', 5.9370, 51.9380), ('Nijmegen Waalbrug', 5.8630, 51.8535),
                       ('Nijmegen rail bridge', 5.8525, 51.8520), ('Arnhem road bridge', 5.9110, 51.9760), ('Driel ferry', 5.8190, 51.9740)]:
    x, y = inv * tr.transform(lon, lat)
    cv2.drawMarker(im, (int(x), int(y)), (200, 0, 200), cv2.MARKER_TILTED_CROSS, 24, 2)
    cv2.putText(im, name, (int(x)+12, int(y)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 0, 200), 2)
cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 80]); print('wrote', out)
