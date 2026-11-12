#!/usr/bin/env python3
"""Run locally: python migrate_tvou_images.py TVOU-Art-GitHub-Pages.zip"""
import hashlib
import mimetypes
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('TVOU-Art-GitHub-Pages.zip')
OUTPUT = SOURCE.parent / 'TVOU-Art-GitHub-Pages-Migrated.zip'
REPORT = SOURCE.parent / 'TVOU-image-migration-report.txt'
PATTERN = re.compile(r'https?://(?:static|64\.media)\.tumblr\.com/[^\s"\'<>\\)]+')
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; TVOUArtMigration/1.0)'}

def download(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
        content_type = response.headers.get('Content-Type', '').split(';')[0].strip().lower()
    if not data or content_type.startswith('text/') or content_type == 'application/json':
        raise ValueError('Unexpected response: ' + content_type)
    return data, content_type

if not SOURCE.exists():
    sys.exit('Cannot find input ZIP: ' + str(SOURCE))
with zipfile.ZipFile(SOURCE) as archive:
    files = {name: archive.read(name) for name in archive.namelist() if not name.endswith('/')}

html_names = [name for name in files if name.lower().endswith('.html')]
urls = sorted({url for name in html_names for url in PATTERN.findall(files[name].decode('utf-8'))})
print('Found', len(urls), 'unique Tumblr image URLs.')
replacements = {}
images = {}
failures = {}
for i, url in enumerate(urls, 1):
    try:
        data, content_type = download(url)
        path = urllib.parse.urlsplit(url).path
        extension = Path(path).suffix.lower()
        if extension not in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.svg'):
            extension = mimetypes.guess_extension(content_type) or '.jpg'
        name = 'assets/images/' + hashlib.sha256(url.encode()).hexdigest()[:16] + extension
        images[name] = data
        replacements[url] = '/' + name
        print(f'[{i}/{len(urls)}] OK {name} ({len(data):,} bytes)')
    except Exception as error:
        failures[url] = str(error)
        print(f'[{i}/{len(urls)}] FAILED {url}: {error}')
    time.sleep(0.1)

for name in html_names:
    html = files[name].decode('utf-8')
    for old, new in replacements.items():
        html = html.replace(old, new)
    files[name] = html.encode('utf-8')

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, data in {**files, **images}.items():
        archive.writestr(name, data)

lines = [f'Unique Tumblr images found: {len(urls)}', f'Downloaded: {len(replacements)}', f'Failed: {len(failures)}', '', 'Unmigrated image URLs:']
lines.extend(f'{url}\n  {error}' for url, error in failures.items())
REPORT.write_text('\n'.join(lines), encoding='utf-8')
print('\nCreated:', OUTPUT)
print('Report:', REPORT)
if failures:
    print('WARNING: Some images could not be downloaded. Original Tumblr links remain for those images.')
else:
    print('SUCCESS: All Tumblr image links in HTML were replaced with local GitHub image paths.')
