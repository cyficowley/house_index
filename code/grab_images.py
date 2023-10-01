# Use /usr/bin/python3
import cv2
import urllib.request
import numpy as np
import asyncio


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
        print(f"img_num {img_num} similarities {similarities}, blur {blur_num}")

        cv2.imwrite(f"./../frames/asdf_{img_num}.jpg", img)

    for i, best in enumerate(picked_images):
        cv2.imwrite(f"./../frames/best_{i}.jpg", best[0])

    return [best_pair[0] for best_pair in picked_images]


async def get_api_response_for_images(images):
    print("yeet")


BATCH_SIZE = 20


def start_image_grabbing_process():
    stream = urllib.request.urlopen("http://192.168.7.2:8081/")
    bytes = bytes()
    img_num = 0
    images = []
    last_api_response = None
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b"\xff\xd8")
        b = bytes.find(b"\xff\xd9")
        if a != -1 and b != -1:
            jpg = bytes[a : b + 2]
            bytes = bytes[b + 2 :]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            images.append(img)
            if last_api_response is not None:
                if not last_api_response.done():
                    images = []
                    continue

            img_num += 1

            if img_num == BATCH_SIZE:
                final_images = pick_best_pics(images)
                last_api_response = asyncio.create_task(
                    get_api_response_for_images(final_images)
                )
                images = []
                img_num = 0
