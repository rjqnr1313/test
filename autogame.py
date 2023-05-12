import pyautogui, os, time
from PIL import ImageChops

y_pos = 277
high = 920 - y_pos
width = 971 - 519

src = pyautogui.screenshot(region=(519, y_pos, width, high))
src.save('src.jpg')
dest = pyautogui.screenshot(region=(971, y_pos, width, high))
dest.save('dest.jpg')
diff = ImageChops.difference(src,dest)
diff.save('diff.jpg')


while not os.path.exists('diff.jpg'):
    time.sleep(1)

import cv2
src_img = cv2.imread('src.jpg')
dest_img = cv2.imread('dest.jpg')
diff_img = cv2.imread('diff.jpg')

gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
gray = (gray > 25) * gray # 이 줄 추가
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

COLOR = (0, 200, 0)
for cnt in contours:
    if cv2.contourArea(cnt) > 50:
        x, y, width, high = cv2.boundingRect(cnt)
        cv2.rectangle(src_img, (x,y),(x + width, y + high), COLOR, 2)
        cv2.rectangle(dest_img, (x,y),(x + width, y + high), COLOR, 2)
        cv2.rectangle(diff_img, (x,y),(x + width, y + high), COLOR, 2)

        to_x = x + (width // 2 ) + 519
        to_y = y + (high // 2) + y_pos
        pyautogui.moveTo(to_x, to_y, duration = 0.3)
        pyautogui.click(to_x, to_y)


cv2.imshow('src', src_img)
cv2.imshow('dest', dest_img)
cv2.imshow('diff', diff_img)