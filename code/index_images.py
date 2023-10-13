from nltk.stem.lancaster import LancasterStemmer
import os
from modify_image import bb_image
from image import Image
import redis
import json
import pickle


RECENT_IMAGES_PER_TERM = 5

IMAGE_DIR_PREFIX = "image_dir"


IMAGE_LIST_NAME = "image_list_key_no_collision"


class ImageDatabase:
    def get_image_list(self):
        if not self.redis.exists(IMAGE_LIST_NAME):
            return []
        return pickle.loads(self.redis.get(IMAGE_LIST_NAME))

    def set_image_list(self, image_list):
        self.redis.set(IMAGE_LIST_NAME, pickle.dumps(image_list))

    def append_image_list(self, image: Image):
        image_list = self.get_image_list()
        length = len(image_list)
        image_list.append(image)
        self.set_image_list(image_list)
        return length

    def get_term_image_indexes(self, term_name):
        return json.loads(self.redis.get(term_name))

    def set_term_image_indexes(self, term_name, term_indexes):
        self.redis.set(term_name, json.dumps(term_indexes))

    def __init__(self):
        self.redis = redis.Redis(host="localhost", port=6379, decode_responses=False)
        self.stemmer = LancasterStemmer()

        i = 0
        while True:
            dir_path = os.path.join("static", "tempdir", f"{IMAGE_DIR_PREFIX}_{i}")
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
                break
            i += 1

        self.dir_path = dir_path

    def add_image(self, metadata_response, time_stamp, image_data):
        (terms, term_to_bbox) = self.process_response_metadata(metadata_response)
        print("adding image with terms ", terms)

        stemmed_terms = [self.stemmer.stem(term) for term in terms]

        index = self.append_image_list(
            Image(self.dir_path, stemmed_terms, term_to_bbox, time_stamp, image_data)
        )

        for term in stemmed_terms:
            term_to_image_index = []
            if self.redis.exists(term):
                term_to_image_index = self.get_term_image_indexes(term)
            term_to_image_index.append(index)
            self.set_term_image_indexes(term, term_to_image_index)

    def process_response_metadata(self, metadata_response):
        term_to_bbox = {}
        # TODO maybe filter the low logit/confidense?
        for bbox in metadata_response["result"]["mask"]:
            if bbox["label"] == "background":
                continue
            terms = [self.stemmer.stem(term) for term in bbox["label"].split(" ")]
            for term in terms:
                if term not in term_to_bbox:
                    term_to_bbox[term] = []
                term_to_bbox[term].append({"box": bbox["box"], "value": bbox["value"]})

        return (list(term_to_bbox.keys()), term_to_bbox)

    def get_images_for_query(self, query):
        query_term_list = query.split(" ")

        stemmed_terms = [self.stemmer.stem(term) for term in query_term_list]

        return_term_indexes = []

        for term in stemmed_terms:
            if not self.redis.exists(term):
                continue

            image_indexes = self.get_term_image_indexes(term)
            # If I want to return multiple, here
            num_results = len(image_indexes)
            for i in range(0, min(num_results, 3)):
                return_term_indexes.append((term, image_indexes[-(i + 1)]))

        image_list = self.get_image_list()
        final_list = [
            (term, image_list[index]) for (term, index) in return_term_indexes
        ]

        return final_list

    def get_bounding_box_paths_for_query(self, query):
        final_image_terms = self.get_images_for_query(query)
        final_paths = []
        for (term, image) in final_image_terms:
            final_paths.append(bb_image(image, term))

        return final_paths
