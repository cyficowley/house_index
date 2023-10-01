import cv2
from datetime import datetime
import random
import os


class Image:
    def __init__(
        self, path_prefix, terms, term_to_bbox, time_stamp, image_data
    ) -> None:
        self.terms = terms
        self.time_stamp = time_stamp
        self.name = f"term-{'-'.join(terms)}_date-{datetime.fromtimestamp(time_stamp).strftime('%Y%m%d-%H%M%S',)}_{random.randint(0, 100)}.jpg"
        self.path = os.path.join(path_prefix, self.name)
        self.term_to_bbox = term_to_bbox
        cv2.imwrite(self.path, image_data)

    def read_image(self):
        return cv2.imread(self.path)
