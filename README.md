# Dreamscapes

This is a Flask-based web application that provides dream interpretation and visualization services. The application leverages OpenAI's powerful GPT-4 model to interpret dreams and generate dream descriptions, enhancing the overall experience for users interested in exploring the meaning of their dreams. The users can also maintain a dream journal by using this app.

### Features:

#### 0. Dream Description Input:

Users can describe their dream in natural language, providing details like settings, characters, emotions, and events.

#### 1. Dream Composer:

The app processes the input and generates a vivid and detailed description of the dream. It adds imaginative elements, subtle nuances, and emotional context to enhance the dream narrative.

#### 2. Visual Dream Rendering:

The app creates a visual representation of the dream. The generated image reflects the dreamer's description, incorporating multiple elements.

#### 3. Dream Interpretation
Users can request the app to interpret their dreams in a manner similar to a psychologist. The interpretation includes insights into the user's current state of mind.

#### 4. Sentiment Analysis
The app performs sentiment analysis on the input text using Hugging Face's pretrained model. It provides information on the sentiment's label (positive, negative, or neutral) and a corresponding confidence score.

#### 5. Dream Journal
Users can maintain a journal of their dreams. 

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

### Disclaimer
This app is not a substitute for professional advice, diagnosis, or treatment provided by a qualified psychologist or mental health professional. Always seek the advice of your mental health provider with any questions you may have regarding a medical condition. 


### Future Improvements
Implementing user authentication for secure dream journaling.\
Allowing users to delete or edit their journal entries.\
Enhancing the UI/UX for a more interactive experience.

### Acknowledgments
OpenAI for providing the powerful GPT-4 model.\
Hugging Face for the sentiment analysis NLP model.
