"""
This module implements a Flask-RESTful API for text generation using OpenAI's GPT-4 model.
"""

import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and Flask-RESTful API
app = Flask(__name__)
api = Api(app)

# Initialize OpenAI client with API key from environment variables
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class GPTTextGenerator(Resource):
    """
    A resource class for generating text using OpenAI's GPT-4 model.
    """

    def __init__(self):
        """
        Initialize the request parser for the resource.
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('prompt', type=str, required=True, 
                                   help='No prompt provided', location='json')
        super(GPTTextGenerator, self).__init__()

    def post(self):
        """
        Handle POST requests to generate text based on the provided prompt.
        """
        args = self.reqparse.parse_args()
        prompt = args['prompt']

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )
            
            content = response.choices[0].message.content
            model = response.model
            usage = {
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens
            }
            return {"content": content, "model": model, "usage": usage}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

# Add the resource to the API
api.add_resource(GPTTextGenerator, '/generate')

if __name__ == '__main__':
    app.run(debug=True)