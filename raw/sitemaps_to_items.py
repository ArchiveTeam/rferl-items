import gzip
import os
import re
import typing

import zstandard


def ids(filename: str) -> typing.Iterator[typing.Tuple[str, int]]:
    print('Processing', filename)
    with (gzip.open if filename.endswith('.gz') else open)(filename, 'rb') as f:
        yield from re.findall(r'https?://([^/]+)/a/[^/]*?/?([0-9]+)\.html', str(f.read(), 'utf8'))


def main():
    for directory in os.listdir('sitemaps'):
        dirpath = os.path.join('sitemaps', directory)
        if not os.path.isdir(dirpath):
            continue
        items = set()
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            for site, identifier in ids(filepath):
                if site.startswith('www.'):
                    site = site.split('.', 1)[1]
                items.add('article:{}:{}'.format(identifier, site))
        with zstandard.open(directory+'_items.txt.zst', 'w') as f:
            f.write('\n'.join(items)+'\n')

if __name__ == '__main__':
    main()

