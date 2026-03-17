#!/usr/bin/env python3
"""Copy resized icons to Android mipmap folders."""
import os, shutil

mapping = {
    'mipmap-mdpi':    72,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

base = 'android/app/src/main/res'
for folder, size in mapping.items():
    src = f'icons/icon-{size}.png'
    dst_dir = f'{base}/{folder}'
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src, f'{dst_dir}/ic_launcher.png')
    shutil.copy(src, f'{dst_dir}/ic_launcher_round.png')
    print(f'Copied icon-{size}.png -> {dst_dir}/')

print('Done.')
