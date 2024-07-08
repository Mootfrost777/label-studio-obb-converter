import cv2
import os
import sys
from pathlib import Path
import random


labels = os.path.join(sys.argv[1], 'labels')
files = os.listdir(labels)
file = random.choice(files)
frame = cv2.imread(os.path.join(sys.argv[1], 'images', Path(file).stem + '.jpg'))
height, width, channels = frame.shape


with open(os.path.join(labels, file)) as f:
    for line in f.readlines():
        data = list(map(float, line.split()))
        print(data)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for i in range(1, len(data), 2):
            cv2.circle(frame, (round(data[i] * width), round(data[i + 1] * height)), 3, color, 2)


cv2.imshow("Input", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

