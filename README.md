# Dreamscapes

This is a Flask-based web application that provides interpretation and visualization of a user's dream. The application leverages OpenAI's powerful GPT-4 model to interpret dreams and generate dream descriptions, enhancing the overall experience for users interested in exploring the meaning of their dreams. The users can also maintain a dream journal by using this app.

### Features:

#### 0. Dream Description Input:

Users can describe their dream in natural language, providing details like settings, characters, emotions, and events.

#### 1. Dream Composer:

The app processes the input and generates a vivid and detailed description of the dream. It adds imaginative elements, subtle nuances, and emotional context to enhance the dream narrative. Uses GPT-4.

#### 2. Visual Dream Rendering:

The app creates a visual representation of the dream. The generated image reflects the dreamer's description, incorporating multiple elements. Uses DALL·E (GPT-3).

#### 3. Dream Interpretation
Users can request the app to interpret their dreams in a manner similar to a psychologist. The interpretation includes insights into the user's current state of mind. Uses GPT-4.

#### 4. Sentiment Analysis
The app performs sentiment analysis on the input text using Hugging Face's pretrained BERT model. It provides information on the sentiment's label (positive, negative, or neutral) and a corresponding confidence score.

#### 5. Dream Journal
Users can maintain a journal of their dreams. They can search for a specific dream entry in their journal.

#### 6. Recommendation Engine
This app utilizes pre-trained Bidirectional Encoder Representations from Transformers (BERT) models to generate book recommendations based on user's dream.\
We are utilizing the CMU Books Dataset. After performing the initial processing of the dataset, we generate embeddings for each book summary and the user's dream using pre-trained BERT model. We find the three most similar book descriptions to the user's dream using Cosine similarity.

### Dependencies

This project requires Python 3.8+ and the Python libraries required can be found here:\
[requirements.txt](https://github.com/Renalka/Dreamscapes/blob/main/requirements.txt)

### Setup

1. Clone the repository to your local machine.
```bash
git clone https://github.com/Renalka/Dreamscapes.git
```

2. Ensure you have the required dependencies installed.
```bash
pip install -r requirements.txt
```

3. Obtain an API key from OpenAI. Create a .env file in the root directory and save the key in your environment variables as OPENAI_API_KEY.

4. Open a terminal and initialize the Database.

```bash
from app import db
db.create_all()
exit()
```
  Check  if the database was created successfully.
```bash
sqlite3 dreamscape_test.db
```
  Create a table inside the database.
```sqlite3
CREATE TABLE dream (
    id INTEGER PRIMARY KEY,
    content TEXT,
    date DATETIME
);
```

5. Run the Flask application:
```bash
python app.py
```

6. Visit http://localhost:5000 in your web browser.

### Database
The application uses SQLite as the database to store dream entries. The database schema contains the following fields:

id: Integer, primary key\
content: Text, the dream content\
date: DateTime, the date and time the dream was recorded

### Dataset for Recommendation System
The CMU Books Dataset is a comprehensive collection of book-related information curated by Carnegie Mellon University. Here are the key attributes included in the CMU Books Dataset:

Book ID: A unique identifier assigned to each book in the dataset.\
Freebase ID: A reference identifier associated with books in the Freebase knowledge graph.\
Book Title: The title of the book, which serves as a primary identifier for individual works.\
Author: The name of the author(s) responsible for writing the book.\
Publication Date: The date when the book was published.\
Genre: The genre or category to which the book belongs, providing insights into its thematic content.\
Summary: A concise textual description or summary of the book's content. These summaries are typically short paragraphs that capture the essence of the story or subject matter.

### Disclaimer
This app is not a substitute for professional advice, diagnosis, or treatment provided by a qualified psychologist or mental health professional. Always seek the advice of your mental health provider with any questions you may have regarding a medical condition. 


### Future Improvements
Implementing user authentication for secure dream journaling.\
Allowing users to delete or edit their journal entries.\
Enhancing the UI/UX for a more interactive experience.

### Acknowledgments
OpenAI for providing the powerful GPT-4 model.\
Hugging Face for the sentiment analysis NLP model.\
Carnegie Mellon University for curating and providing the CMU Books Dataset.
