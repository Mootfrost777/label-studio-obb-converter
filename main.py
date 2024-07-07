from math import sin, cos, radians
import cv2

frame = cv2.imread('img.png')

height, width, channels = frame.shape

x = 0.42
y = 0.59
w = 0.67
h = 0.03
r = radians(327)


print(width, height, x, y, w, h)


def transform(c, cz, a: float):
    cn = c[0] - cz[0], c[1] - cz[1]
    cn = round(cn[0] * cos(a) - cn[1] * sin(a)), round(cn[0] * sin(a) + cn[1] * cos(a))
    # return cn[0] + cz[0], cn[1] + cz[1]
    return cn[0] + cz[0], cn[1] + cz[1]


cv2.circle(frame, (0, 0), 3, (0, 0, 255), 2)

c1, c2, c3, c4 = [round(x * width), round(y * height)], [round((x + w) * width), round(y * height)], [round(x * width), round((y + h) * height)], [round((x + w) * width), round((y + h) * height)]

col1 = (0, 255, 0)
col2 = (255, 255, 0)


cv2.rectangle(frame, c1, c4, col1, 2)


cv2.circle(frame, c1, 3, col1, 2)
cv2.circle(frame, c2, 3, col1, 2)
cv2.circle(frame, c3, 3, col1, 2)
cv2.circle(frame, c4, 3, col1, 2)


cn1, cn2, cn3, cn4 = transform(c1, c1, r), transform(c2, c1, r), transform(c3, c1, r), transform(c4, c1, r)

cv2.circle(frame, cn1, 3, col2, 2)
cv2.circle(frame, cn2, 3, col2, 2)
cv2.circle(frame, cn3, 3, col2, 2)
cv2.circle(frame, cn4, 3, col2, 2)

cv2.line(frame, cn1, cn2, col2, 1)
cv2.line(frame, cn2, cn4, col2, 1)
cv2.line(frame, cn4, cn3, col2, 1)
cv2.line(frame, cn1, cn3, col2, 1)


frame = cv2.resize(frame, (width*2, height*2))

cv2.imshow("Input", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

