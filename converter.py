import shutil
import uuid
import os
import sys
import json
import urllib.request
import pathlib
import time
from math import sin, cos, radians




class Label:
    def __init__(self, x, y, width, height, rotation, rectanglelabels, original_width, original_height):
        self.orig_w = original_width
        self.orig_h = original_height
        self.x = x / 100 * self.orig_w
        self.y = y / 100 * self.orig_h
        self.w = width / 100 * self.orig_w
        self.h = height / 100 * self.orig_h
        self.r = radians(rotation)


def transform(c, cs, a):
    cn = c[0] - cs[0], c[1] - cs[1]
    cn = cn[0] * cos(a) - cn[1] * sin(a), cn[0] * sin(a) + cn[1] * cos(a)
    return cn[0] + cs[0], cn[1] + cs[1]


def conv_percent(c, l):
    return c[0] / l.orig_w, c[1] / l.orig_h


def transform_coordinates(l: Label) -> tuple:
    c1, c2, c3, c4 = (l.x, l.y), (l.x + l.w, l.y), (l.x + l.w, l.y + l.h), (l.x, l.y + l.h)
    return conv_percent(c1, l), conv_percent(transform(c2, c1, l.r), l), conv_percent(transform(c3, c1, l.r), l), conv_percent(transform(c4, c1, l.r), l)


print('---------------------')
print('Start')
start_time = time.time()

uid = str(uuid.uuid4())
path = os.path.join('out', uid)
pathlib.Path(os.path.join(path, 'images')).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join(path, 'labels')).mkdir(parents=True, exist_ok=True)


if len(sys.argv) > 2:
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', f'Token {sys.argv[3]}')]
    urllib.request.install_opener(opener)

with open(sys.argv[1]) as f:
    dataset = json.load(f)


labels = []
for obj in dataset:
    if len(sys.argv) > 2:
        url = sys.argv[2] + obj['image']
        name = str(uuid.uuid4())
        urllib.request.urlretrieve(url, os.path.join(path, 'images', name + pathlib.Path(url).suffix))
    else:
        name = obj['image'].split('d=')[-1].split('%5C')[-1]
        shutil.copy(os.path.join('images', name), os.path.join(path, 'images', name))
        name = pathlib.Path(name).stem
    output = []
    if 'label' in obj:
        pass
    else:
        continue

    for label in obj['label']:
        label_name = label['rectanglelabels'][0]
        if label_name not in labels:
            labels.append(label_name)
        cords = transform_coordinates(Label(**label))
        output.append(f'{labels.index(label_name)} {' '.join(' '.join('{:.6f}'.format(y) for y in x) for x in cords)}')
    with open(os.path.join(path, 'labels', name + '.txt'), 'w') as f:
        f.write('\n'.join(output))

with open(os.path.join(path, 'classes'), 'w') as f:
    f.write('\n'.join(labels))


shutil.make_archive(path, format='zip', root_dir=path)
#shutil.rmtree(path)

print(f'Completed in: {time.time() - start_time}')
print(f'Saved as {path}.zip')
print('---------------------')

