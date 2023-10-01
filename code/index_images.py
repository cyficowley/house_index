from nltk.stem.lancaster import LancasterStemmer
import os
from modify_image import bb_image
from image import Image


RECENT_IMAGES_PER_TERM = 5

IMAGE_DIR_PREFIX = "image_dir"


class ImageDatabase:
    def __init__(self):
        self.term_to_image_index = {}
        self.images = []
        self.stemmer = LancasterStemmer()

        i = 0
        while True:
            dir_path = os.path.join("tempdir", f"{IMAGE_DIR_PREFIX}_{i}")
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
                break
            i += 1

        self.dir_path = dir_path

    def add_image(self, metadata_response, time_stamp, image_data):
        (terms, term_to_bbox) = self.process_response_metadata(metadata_response)

        index = len(self.images)
        stemmed_terms = [self.stemmer.stem(term) for term in terms]
        self.images.append(
            Image(self.dir_path, stemmed_terms, term_to_bbox, time_stamp, image_data)
        )

        for term in stemmed_terms:
            if term not in self.term_to_image_index:
                self.term_to_image_index[term] = []
            index_list = self.term_to_image_index[term]
            if len(index_list) == RECENT_IMAGES_PER_TERM:
                index_list.pop(0)
            index_list.append(index)

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
            if term not in self.term_to_image_index:
                continue

            image_indexes = self.term_to_image_index[term]
            # If I want to return multiple, here
            return_term_indexes.append((term, image_indexes[-1]))

        return [(term, self.images[index]) for (term, index) in return_term_indexes]

    def get_bounding_box_paths_for_query(self, query):
        final_image_terms = self.get_images_for_query(query)
        final_paths = []
        for (term, image) in final_image_terms:
            final_paths.append(bb_image(image, term))

        return final_paths
