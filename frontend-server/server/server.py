from flask import Flask, request, jsonify, after_this_request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import openai

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    # response = openai.Completion.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt= f'I\'m going to give you some questions that someone has about their items. For each question, I want you to give me a comma seperated list of the one or many items I\'m asking about in a list snippet. For example \'where are my keys and wallet?\' and respond \'keys, wallet\'. Here is what I\'m asking about: {args["query"]}"',
    #     temperature=0.6
    # )

    
    return {'images':['https://snowdoniadonkeys.com/wp-content/uploads/2023/01/Nel-2-scaled.jpg' for _ in range(15)]}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
