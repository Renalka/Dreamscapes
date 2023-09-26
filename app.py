from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
import openai

import os

key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initializing OpenAI API client
openai.api_key = key

dreams_database = []

@app.route('/generate_dream', methods=['POST'])
def generate_dream():
    user_input = request.json.get('user_input')

    # Generating dream description using OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=150,
        temperature=0.6,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    dream_description = response.choices[0].text.strip()

    # Generating image
    generated_image_url = generate_image(dream_description)

    # Saving dream to the list
    dreams_database.append({'dream_description': dream_description, 'image_url': generated_image_url})

    return jsonify({'dream_description': dream_description, 'image_url': generated_image_url})

def generate_image(dream_description):
    # Using OpenAI's API to generate an image based on the dream description

    response = openai.Image.create(prompt=dream_description, n=1, size="1024x1024")
    image_url = response['data'][0]['url']

    return image_url


if __name__ == '__main__':
    app.run(debug=True)
