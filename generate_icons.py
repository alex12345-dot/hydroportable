#!/usr/bin/env python3
"""Generate app icons for Moto Uniforme."""

import os
import struct
import zlib

def create_png(size):
    """Create a simple PNG with a water drop icon."""
    width = height = size
    # Purple-blue gradient background with water drop
    bg_r, bg_g, bg_b = 102, 126, 234  # #667eea

    # Build raw pixel data (RGBA)
    pixels = []
    cx, cy = width / 2, height / 2
    r = width * 0.42

    for y in range(height):
        row = []
        for x in range(width):
            # Circular background
            dx, dy = x - cx, y - cy
            dist = (dx**2 + dy**2) ** 0.5

            if dist <= r:
                # Blend gradient
                t = y / height
                pr = int(bg_r + t * (118 - bg_r))
                pg = int(bg_g + t * (75 - bg_g))
                pb = int(bg_b + t * (162 - bg_b))

                # Water drop shape (droplet)
                drop_cx = cx
                drop_top = cy - r * 0.55
                drop_bot = cy + r * 0.35
                drop_rx = r * 0.28
                drop_ry = r * 0.38

                # Ellipse body of drop
                in_ellipse = ((x - drop_cx) / drop_rx) ** 2 + ((y - (drop_top + drop_ry)) / drop_ry) ** 2 <= 1

                # Triangle tip (top of droplet points up)
                tip_y = drop_top - drop_ry * 0.6
                rel_y = y - tip_y
                tip_half_w = drop_rx * 0.55
                if tip_y <= y <= drop_top + drop_ry and abs(x - drop_cx) <= tip_half_w * (1 - rel_y / (drop_top + drop_ry - tip_y + 0.001)):
                    in_drop = True
                else:
                    in_drop = in_ellipse

                if in_drop:
                    row.extend([255, 255, 255, 220])
                else:
                    row.extend([pr, pg, pb, 255])
            else:
                row.extend([0, 0, 0, 0])
        pixels.append(bytes(row))

    def make_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)

    # IDAT
    raw = b''.join(b'\x00' + row for row in pixels)
    compressed = zlib.compress(raw, 9)
    idat = make_chunk(b'IDAT', compressed)

    # IEND
    iend = make_chunk(b'IEND', b'')

    return sig + ihdr + idat + iend


os.makedirs('icons', exist_ok=True)

sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for s in sizes:
    data = create_png(s)
    path = f'icons/icon-{s}.png'
    with open(path, 'wb') as f:
        f.write(data)
    print(f'Created {path} ({s}x{s})')

print('Done! Icons saved to icons/')
