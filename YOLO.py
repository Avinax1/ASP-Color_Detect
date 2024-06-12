from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2

IMAGE_FILE = 'picture.jpg'
img = cv2.imread(IMAGE_FILE)
img_an = None

model = YOLO('yolov8n-oiv7.pt')
results = model.predict(img,device='cpu')

for obj in results:
    annotator = Annotator(img, line_width=2, font_size=10)
    boxes = obj.boxes
    for box in boxes:
        label = model.names[int(box.cls)] + "(" + str(round(float(box.conf[0]), 2)) + ")"
        annotator.box_label(box.xyxy[0], label)
    img_an = annotator.result()

cv2.imwrite('result.jpg', img_an)
