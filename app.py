from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from recommendation_engine.recommend import recommend_books
from transformers import pipeline
import requests
import openai
import os

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initializing OpenAI API client
openai.api_key = key

# Sentiment analysis model from Hugging Face
nlp = pipeline("sentiment-analysis") # using the default model="distilbert-base-uncased"

# Setting up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dreamscape_test.db' 
db = SQLAlchemy(app)


class Dream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    try:
        action = request.form['action']
        dream_input = request.form['dream_input']
        #print(dream_input)
        # Saving dream to the database
        new_dream = Dream(content=dream_input)
        db.session.add(new_dream)
        db.session.commit()
        #print(new_dream)
        
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
            generated_image_url = generate_image(dream_input)
            
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
        
        elif action == 'recommend':
            # Recommending books based on dream of the user
            books = recommend_books(dream_input)
            # print(recommended_books)
            recommended_books = [f"{title} by {author}" for title, author in books]
            return render_template('recommended_books.html', recommended_books=recommended_books)
            
    except Exception as e:
        return f"An error occurred: {e}", 500

def generate_image(dream_input):
    try:
        # Using OpenAI's API to generate an image based on the dream description
        response = openai.Image.create(prompt=dream_input, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/dream_journal', methods=['GET', 'POST'])
def dream_journal():
    if request.method == 'POST':
        search_term = request.form['search_term']
        dreams = Dream.query.filter(Dream.description.like(f'%{search_term}%')).all()
    else:
        dreams = Dream.query.all()
    
    return render_template('dream_journal.html', dreams=dreams)



if __name__ == '__main__':
    app.run(debug=True)
