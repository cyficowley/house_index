import cv2
import requests

import json

# im1 = cv2.imread("/Users/cyficowley/Documents/house_index/frames/asdf_0.jpg")

# im1.resize([2,2,2])

# im1 = cv2.resize(im1, (20, 20))

# print(len(json.dumps({"img": im1.tolist()})))

with open(
    "/Users/cyficowley/Documents/house_index/frames/asdf_0.jpg", "rb"
) as image_file:
    response = requests.post(
        "https://wm4uy0lywetgeb-5000.proxy.runpod.net/gangsta_inference",
        files={"image": image_file},
    )


# print(len(json.dumps({"img": im1.tolist()})))

print(len(response.request.body))

print(response)
print(response.json())
