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

@app.route('/generate_dream', methods=['POST'])
def generate_dream():
    #user_input = request.json.get('user_input')
    dream_input = request.form['dream_input']

    # Generating dream description using OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        #prompt=user_input,
        prompt=dream_input,
        max_tokens=200,
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

    #return jsonify({'dream_description': dream_description, 'image_url': generated_image_url})
    return render_template('dream.html', dream=dream_description, image_url=generated_image_url)

def generate_image(dream_description):
    # Using OpenAI's API to generate an image based on the dream description

    response = openai.Image.create(prompt=dream_description, n=1, size="1024x1024")
    image_url = response['data'][0]['url']

    return image_url


@app.route('/interpret_dream', methods=['POST'])
def interpret_dream():
    #dream_description = request.json.get('dream_description')
    dream_description = request.form['dream_description']

    # Generating dream description using OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        #prompt=user_input,
        prompt=f"Act as a psychologist would and interpret this dream. Make sure to talk about the current state of mind the person seems to be in. Dream: {dream_description}",
        max_tokens=200,
        temperature=0.6,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    interpretation = response.choices[0].text.strip()

    #return interpretation
    return render_template('dream_interpretation.html', interpretation=interpretation)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    dream_description = request.form['dream_description']
    #dream_description = request.json.get('dream_description')

    # Using OpenAI's sentiment analysis model to analyze sentiment
    response = openai.Completion.create(
        engine="text-davinci-003",
        #prompt=user_input,
        prompt=f"Detailed sentiment analysis in one or two sentences of the following text:\n {dream_description}",
        max_tokens=200,
        temperature=0.6,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    sentiment = response.choices[0].text.strip()

    #Using HuggingFace's pretrianed model to perform sentiment analysi
    sentiment_result = nlp(dream_description)[0]
    sentiment_label = sentiment_result['label']
    sentiment_score = sentiment_result['score']

    #print(response)
    #return jsonify({'sentiment': sentiment, 'sentiment_label': sentiment_label, 'sentiment_score': sentiment_result['score']})
    return render_template('dream_sentiment.html', sentiment_label=sentiment_label, sentiment_score=sentiment_score, sentiment=sentiment)


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
