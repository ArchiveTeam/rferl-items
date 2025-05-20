import os
import re

import requests
import zstandard


def get_max_id(site: str) -> int:
    response = requests.get('https://{}/'.format(site), timeout=10)
    assert response.status_code == 200
    return max({int(s) for s in re.findall(r'/a/[^/]*?/?([0-9]+)\.html', response.text)} | {-1})
    


def main():
    max_id = 0
    with open('rferlsites.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            temp_id = get_max_id(line)
            print(temp_id, line)
            if temp_id > max_id:
                max_id = temp_id
    print('Found global max ID', max_id)
    old_max_id = 0
    for filename in os.listdir('added'):
        if filename.startswith('article_'):
            temp_id = int(filename.split('.')[0].split('-')[1])
            if temp_id > old_max_id:
                old_max_id = temp_id
    print('Found previous max ID', old_max_id)
    if max_id > old_max_id:
        with zstandard.open('article_{}-{}.txt.zst'.format(old_max_id+1, max_id), 'w') as f:
            for i in range(old_max_id+1, max_id+1):
                f.write('article:{}\n'.format(i))

if __name__ == '__main__':
    main()

