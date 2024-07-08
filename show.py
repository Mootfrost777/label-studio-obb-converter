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
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        for i in range(1, len(data), 2):
            color = colors[(i - 1) // 2]
            cv2.circle(frame, (round(data[i] * width), round(data[i + 1] * height)), 3, color, 2)
            cv2.putText(frame, str((i - 1) // 2), (round(data[i] * width) - 5, round(data[i + 1] * height) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)


cv2.imshow("Input", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

