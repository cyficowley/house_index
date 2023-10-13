from flask import Flask, request
from flask_cors import CORS
import openai
import os
from multiprocessing import Process
from grab_images import start_image_grabbing_process
from index_images import ImageDatabase
import multiprocessing

app = Flask(__name__)
CORS(app)


# delete


# import sys
# import time
# import cv2
# import json

# sys.path.append("/Users/cyficowley/Documents/house_index/code")


# first_terms = ["keys", "dog", "sandals"]
# second_terms = ["oranges", "tangerines", "sandals"]

# im1 = cv2.imread("/Users/cyficowley/Documents/house_index/frames/asdf_0.jpg")
# with open("/Users/cyficowley/Downloads/gangsta_response.json") as file:
#     response_metadata_1 = json.load(file)
# im2 = cv2.imread("/Users/cyficowley/Documents/house_index/frames/asdf_1.jpg")
# with open("/Users/cyficowley/Downloads/gangsta_response_2.json") as file:
#     response_metadata_2 = json.load(file)

# image_database.add_image(response_metadata_1, time.time(), im1)

# image_database.add_image(response_metadata_2, time.time(), im2)


# delete
image_database = ImageDatabase()


@app.route("/search", methods=["GET"])
def search():
    args = request.args
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = "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"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f'I\'m going to give you some questions that someone has about their items. For each question, I want you to give me a comma seperated list of the one or many items I\'m asking about in a list snippet. For example \'where are my keys and wallet?\' and respond \'keys, wallet\'. Here is what I\'m asking about: {args["query"]}"',
        temperature=0.6,
    )

    query = response["choices"][0]["text"].strip()

    print(query)

    # print("What went wrong", image_database.term_to_image_index)
    # print("Adding with id ", id(image_database))

    return {
        "chat_res": response,
        "images": [
            f"http://127.0.0.1:5000/{p}"
            for p in image_database.get_bounding_box_paths_for_query(query)
        ],
        "query": query,
    }


if __name__ == "__main__":
    global p
    p = Process(target=start_image_grabbing_process)
    p.start()
    app.run(host="127.0.0.1", port=5000)
