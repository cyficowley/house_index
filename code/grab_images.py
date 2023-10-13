# Use /usr/bin/python3
import cv2
import urllib.request
import numpy as np
import asyncio
import requests
from index_images import ImageDatabase
import time


def laplacian(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()


def get_image_similarity(gram_a, gram_b):
    return cv2.compareHist(gram_a, gram_b, cv2.HISTCMP_BHATTACHARYYA)


def get_image_histograms(images):
    grams = []
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists
    for img in images:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        channels = [0, 1]
        gram = cv2.calcHist([hsv], channels, None, histSize, ranges, accumulate=False)
        cv2.normalize(gram, gram, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        grams.append(gram)
    return grams


DIFF_THRESHOLD = 0.4

BLUR_THRESHOLD = 2023


def pick_best_pics(images):
    histograms = get_image_histograms(images)
    image_hist_pairs = list(zip(images, histograms))
    blurs = [(laplacian(img), i) for (i, img) in enumerate(images)]
    sorted_blurs = sorted(blurs)[::-1]

    picked_images = []

    for img_num, (blur_num, img_index) in enumerate(sorted_blurs):
        img, hist = image_hist_pairs[img_index]
        similarities = [
            get_image_similarity(hist, best_img[1]) for best_img in picked_images
        ]
        if (
            all([sim > DIFF_THRESHOLD for sim in similarities])
            and blur_num > BLUR_THRESHOLD
        ):
            picked_images.append(image_hist_pairs[img_index])
        # print(f"img_num {img_num} similarities {similarities}, blur {blur_num}")

        # cv2.imwrite(f"./../frames/asdf_{img_num}.jpg", img)

    # for i, best in enumerate(picked_images):
    #     cv2.imwrite(f"./../frames/best_{i}.jpg", best[0])

    return [best_pair[0] for best_pair in picked_images]


def write_api_responses_to_database(images, image_database: ImageDatabase):
    print("TRYINA DO THIS??")
    for image in images:
        print("TRYINA DO THIS 2??")
        cv2.imwrite("/tmp/written_img.jpg", image)
        with open("/tmp/written_img.jpg", "rb") as image_file:
            print("MADE REQUEST")
            response = requests.post(
                "https://wm4uy0lywetgeb-5000.proxy.runpod.net/gangsta_inference",
                files={"image": image_file},
            )
            repsonse_metadata = response.json()
            print("ADDED IMAGE")
            print("Adding with id ", id(image_database))
            image_database.add_image(repsonse_metadata, time.time(), image)


BATCH_SIZE = 1


def start_image_grabbing_process():
    stream = urllib.request.urlopen("http://192.168.0.68:8081/")
    bytes_stream = bytes()
    img_num = 0
    images = []
    last_api_response = None
    image_database = ImageDatabase()
    while True:
        bytes_stream += stream.read(1024)
        a = bytes_stream.find(b"\xff\xd8")
        b = bytes_stream.find(b"\xff\xd9")
        if a != -1 and b != -1:
            print("Captured image")
            jpg = bytes_stream[a : b + 2]
            bytes_stream = bytes_stream[b + 2 :]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            images.append(img)
            if img_num % 3 == 0:
                write_api_responses_to_database([img], image_database)

            img_num += 1


# if __name__ == "__main__":
#     start_image_grabbing_process()
