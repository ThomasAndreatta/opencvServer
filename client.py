import requests
import cv2
import numpy as np


url = 'http://192.168.178.106:5000/video'
#url = 'http://<your ip>:5000/video'
resp = requests.get(url)


txt = resp.text

txt = np.array(txt)
print(txt)
cv2.imshow('image',txt)


cv2.waitKey(2000)

cv2.destroyAllWindows()
