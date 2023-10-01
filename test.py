import sys
import time
import cv2
import json

sys.path.append("/Users/cyficowley/Documents/house_index/code")


from code.index_images import ImageDatabase

database = ImageDatabase()


first_terms = ["keys", "dog", "sandals"]
second_terms = ["oranges", "tangerines", "sandals"]

im1 = cv2.imread("/Users/cyficowley/Documents/house_index/frames/asdf_0.jpg")
with open("/Users/cyficowley/Downloads/gangsta_response.json") as file:
    response_metadata_1 = json.load(file)
im2 = cv2.imread("/Users/cyficowley/Documents/house_index/frames/asdf_1.jpg")
with open("/Users/cyficowley/Downloads/gangsta_response_2.json") as file:
    response_metadata_2 = json.load(file)

database.add_image(response_metadata_1, time.time(), im1)

database.add_image(response_metadata_2, time.time(), im2)

results1 = database.get_bounding_box_paths_for_query("I really need to get some keys")
print(results1)


results2 = database.get_bounding_box_paths_for_query("Where in the fuck is my sandal")
print(results2)

results3 = database.get_bounding_box_paths_for_query("I want an orange")
print(results3)

results4 = database.get_bounding_box_paths_for_query("tangerine pleazy weezy")
print(results4)
