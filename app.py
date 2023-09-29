from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from transformers import pipeline
import openai
import os
import requests

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initializing OpenAI API client
openai.api_key = key
dreams_database = []
# Sentiment analysis model from Hugging Face
nlp = pipeline("sentiment-analysis") # using the default model="distilbert-base-uncased"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    action = request.form['action']
    dream_input = request.form['dream_input']
    
    if action == 'generate':
        # Generating dream description using OpenAI's GPT-4
        response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension. I would like you to read the given text, expand upon it and turn it into a storyline of one paragraph."
            },
            {
                "role": "user",
                "content": dream_input
            }
        ])
        dream_description= response['choices'][0]['message']['content']

        # Generating image
        generated_image_url = generate_image(dream_description)
        # Saving dream to the list
        dreams_database.append({'dream_description': dream_description, 'image_url': generated_image_url})

        return render_template('dream.html', dream=dream_description, image_url=generated_image_url)

    elif action == 'interpret':
        # Interpreting dream using OpenAI's GPT-4
        response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Act as a psychologist would and interpret this dream. Make sure to talk about the current state of mind the person seems to be in."
            },
            {
                "role": "user",
                "content": dream_input
            }
        ])
        interpretation= response['choices'][0]['message']['content']

        return render_template('dream_interpretation.html', interpretation=interpretation)
        
    elif action == 'analyze':
        response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Perform detailed sentiment analysis in a few sentences of the given text."
            },
            {
                "role": "user",
                "content": dream_input
            }
        ])
        
        sentiment= response['choices'][0]['message']['content']
        # Using HuggingFace's pretrianed model to perform sentiment analysis
        sentiment_result = nlp(dream_input)[0]
        sentiment_label = sentiment_result['label']
        sentiment_score = sentiment_result['score']

        #print(response)
        #return jsonify({'sentiment': sentiment, 'sentiment_label': sentiment_label, 'sentiment_score': sentiment_result['score']})
        return render_template('dream_sentiment.html', sentiment_label=sentiment_label, sentiment_score=sentiment_score, sentiment=sentiment)


def generate_image(dream_description):
    # Using OpenAI's API to generate an image based on the dream description
    response = openai.Image.create(prompt=dream_description, n=1, size="1024x1024")
    image_url = response['data'][0]['url']

    return image_url


@app.route("/interactive", methods=["POST"])
def interactive():
    input_text = request.json.get('input_text')

    #print(f"Input Text: {input_text}")

    # Generating the AI response
    response = openai.Completion.create(
        engine="davinci",
        prompt=input_text,
        max_tokens=1000,
        temperature=0.7,
        stop=["\n", "\t"],
    )

    #print(f"OpenAI Response: {response}")

    if "choices" in response and response["choices"]:
        # Extracting and cleaning the generated text
        generated_text = response["choices"][0]["text"].strip()
    else:
        generated_text = "No valid response from OpenAI"

    #print(f"Generated Text: {generated_text}")

    return jsonify({"response": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
