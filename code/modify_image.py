from image import Image
import cv2
import os


def bb_image(image: Image, term: str) -> str:
    orig_filename = os.path.basename(image.path)
    base_path = os.path.dirname(image.path)
    filename_bits = os.path.splitext(orig_filename)
    new_filename = filename_bits[0] + "_bb_" + term + filename_bits[1]

    path = os.path.join(base_path, new_filename)

    if os.path.exists(path):
        return path

    image_data = cv2.imread(image.path)

    term_bboxes = image.term_to_bbox[term]
    for bbox in term_bboxes:
        bbox_values = bbox["box"]
        cv2.rectangle(
            image_data,
            (int(bbox_values[0]), int(bbox_values[1])),
            (int(bbox_values[2]), int(bbox_values[3])),
            (0, 255, 0),
            2,
        )

    cv2.imwrite(path, image_data)
    return path


# def segment_image(image: Image, term: str) -> str:
#     orig_filename = os.path.basename(image.path)
#     base_path = os.path.dirname(image.path)
#     filename_bits = os.path.splitext(orig_filename)
#     new_filename = filename_bits[0] + "_" + term

#     path = os.path.join(base_path, new_filename)

#     if os.path.exists(path):
#         return path
