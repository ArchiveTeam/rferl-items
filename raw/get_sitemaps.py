import os
import re
import traceback
import typing

import requests


def get_file(url: str, return_text: bool = False) -> typing.Optional[str]:
    while True:
        print(url)
        try:
            response = requests.get(url, timeout=10)
            break
        except Exception:
            traceback.print_exc()
    site = response.url.split('/')[2]
    directory = os.path.join('sitemaps', site)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, response.url.split('/')[-1]), 'wb') as f:
        f.write(response.content)
    if return_text:
        return response.text


def download_sitemap(site: str):
    index = get_file('https://{}/sitemap.xml'.format(site), return_text=True)
    for url in re.findall(r'<loc>(https?://[^<]+)</loc>', index):
        get_file(url)


def main():
    with open('../rferlsites.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            download_sitemap(line)

if __name__ == '__main__':
    main()

