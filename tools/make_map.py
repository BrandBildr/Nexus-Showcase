#!/usr/bin/env python3
"""Generates tools/partials/world-map.html: a dotted world map (Natural Earth land, public domain)
with gold pins and connection arcs from Plymouth.

Usage: python3 tools/make_map.py path/to/ne_110m_land.geojson
Edit LOCATIONS below to change the pins, then run tools/build.py.
"""
import json, sys
from pathlib import Path

# name, detail line, lat, lon, label side ("l", "r" or "t"); LIVE = places with open vacancies
LOCATIONS = [
    ("Plymouth, UK", "Head office", 50.37, -4.14, "t"),
    ("Romania", "Europe", 44.17, 28.63, "r"),
    ("Nashville, USA", "North America", 36.16, -86.78, "l"),
    ("The Bahamas", "Caribbean", 25.06, -77.35, "r"),
    ("Brazil", "South America", -22.9, -43.2, "r"),
]
LIVE = {"Plymouth, UK", "The Bahamas"}
LAT_TOP, LAT_BOT, LON_L, LON_R = 74, -56, -170, 190
STEP = 2.0
W = (LON_R - LON_L) / STEP
H = (LAT_TOP - LAT_BOT) / STEP

def xy(lat, lon):
    return ((lon - LON_L) / STEP, (LAT_TOP - lat) / STEP)

def inside(pt, ring):
    x, y = pt; c = False; n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def main(src):
    data = json.load(open(src))
    polys = []
    for f in data["features"]:
        g = f["geometry"]
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for p in rings:
            ring = p[0]
            xs = [a for a, b in ring]; ys = [b for a, b in ring]
            polys.append((min(xs), max(xs), min(ys), max(ys), ring))
    dots = []
    lat = LAT_TOP - STEP / 2
    while lat > LAT_BOT:
        lon = LON_L + STEP / 2
        while lon < LON_R:
            L = lon if lon <= 180 else lon - 360
            for x0, x1, y0, y1, ring in polys:
                if x0 <= L <= x1 and y0 <= lat <= y1 and inside((L, lat), ring):
                    x, y = xy(lat, lon); dots.append(f"M{x:.1f} {y:.1f}h0"); break
            lon += STEP
        lat -= STEP
    hx, hy = xy(LOCATIONS[0][2], LOCATIONS[0][3])
    arcs, pins = [], []
    for i, (name, detail, la, lo, side) in enumerate(LOCATIONS):
        x, y = xy(la, lo)
        if i:
            mx, my = (hx + x) / 2, (hy + y) / 2 - abs(hx - x) * 0.28 - 4
            arcs.append(f'<path class="wmap__arc" style="--i:{i}" d="M{hx:.1f} {hy:.1f}Q{mx:.1f} {my:.1f} {x:.1f} {y:.1f}"/>')
        pins.append(
            f'<li class="wmap__pin{" is-hq" if i == 0 else ""} wmap__pin--{side}" style="--x:{x / W * 100:.2f}%;--y:{y / H * 100:.2f}%;--i:{i}">'
            f'<button type="button" class="wmap__dot" aria-describedby="wm-{i}"><span class="sr-only">{name}</span></button>'
            f'<span class="wmap__label" id="wm-{i}"><strong>{name}{" <i class=wmap__live aria-hidden=true></i>" if name in LIVE else ""}</strong><span>{"Recruiting now" if name in LIVE and i else detail}</span></span></li>')
    html = f'''        <div class="wmap" data-map>
          <div class="wmap__frame">
            <div class="wmap__stage">
              <svg class="wmap__svg" viewBox="0 0 {W:.0f} {H:.0f}" aria-hidden="true" focusable="false">
                <path class="wmap__land" d="{"".join(dots)}"/>
                {"".join(arcs)}
              </svg>
              <ul class="wmap__pins" aria-label="Where we work">
                {"".join(pins)}
              </ul>
            </div>
          </div>
          <ul class="wmap__legend" aria-label="Locations">
            {"".join(f'<li><button type="button" data-pin="{i}">{l[0]}</button></li>' for i, l in enumerate(LOCATIONS))}
          </ul>
        </div>
'''
    out = Path(__file__).resolve().parent / "partials" / "world-map.html"
    out.write_text(html, encoding="utf-8")
    print("wrote", out, len(dots), "dots", len(html) // 1024, "KB")

if __name__ == "__main__":
    main(sys.argv[1])
