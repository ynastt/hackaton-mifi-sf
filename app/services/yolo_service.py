import base64
from io import BytesIO

from PIL import Image

from app.config_reader import config
import numpy as np
import cv2
from ultralytics import YOLO


class YOLOClassifier:

    def __init__(self):
        self.model = YOLO(config.YOLO_MODEL_PATH)

    def get_exhibit_label(self, photo_base64):
        image_data = base64.b64decode(photo_base64)
        image = Image.open(BytesIO(image_data))
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        results = self.model.predict(img, imgsz=640, iou=0.5, conf=0.8)
        result = results[0]
        boxes = result.boxes
        for box in boxes:
            class_id = box.cls.item()
            return str(int(class_id))
