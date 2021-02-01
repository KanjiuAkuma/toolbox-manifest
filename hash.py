import hashlib
import json
import glob
import sys
import os

BUF_SIZE = 1024

ignores = [
    '.git',
    'manifest.json',
]


def read_file(path, buf_size=1024):
    with open(path, 'rb') as f:
        buf = f.read(buf_size)
        while buf:
            yield buf
            buf = f.read(buf_size)


def list_files(path, prefix='', ignore=[]):
    files = []

    for f in os.scandir('%s%s' % (path, prefix)):
        name = prefix + f.name
        if name not in ignore:
            if f.is_dir():
                files.extend(list_files(path, prefix=name + '\\'))
            else:
                files.append(name)

    return files


if __name__ == '__main__':
    folder = sys.argv[1]
    if not folder.endswith('\\'):
        folder += '\\'

    print('Creating hash file for %s' % folder)

    files = list_files(folder, ignore=ignores)
    hashs = {}

    for file_name in files:
        sha = hashlib.sha256()
        for batch in read_file('%s%s' % (folder, file_name)):
            sha.update(batch)

        sha_hex = sha.hexdigest()
        rel_path = file_name.replace('\\', '/')
        print('%s: %s' % (rel_path, sha_hex))
        hashs[rel_path] = sha_hex

    json_string = {
        'files': hashs
    }

    json_data = json.dumps(json_string, indent=4)
    print('writing manifest.json...')
    # with open('%s\\manifest.json' % folder, 'w') as file:
    #     json.dump(json_string, file, indent=4)

    print(json_data)
