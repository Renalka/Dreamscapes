import torch
import csv
import numpy as np
import os
import pandas as pd
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

file_path = os.path.join(os.path.dirname(__file__), 'data/booksummaries.txt')
file_path2 = os.path.join(os.path.dirname(__file__), 'book_embeddings.npy')

def recommend_books(user_input):

    # Using pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    data = []

    with open(file_path, 'r') as f:
        reader = csv.reader(f, dialect='excel-tab')
        for row in reader:
            data.append(row)
    df = pd.DataFrame.from_records(data, columns=['book_id', 'freebase_id', 'book_title', 'author', 'publication_date', 'genre', 'summary'])

    book_embeddings = np.load(file_path2)

    # Tokenizing and getting embeddings for user input
    input_tokens = tokenizer(user_input, return_tensors="pt")
    with torch.no_grad():
        input_embeddings = model(**input_tokens).last_hidden_state.mean(dim=1)

    # Using cosine similarity and getting indices of the top 3 most similar book descriptions
    similarities = cosine_similarity(input_embeddings, book_embeddings)
    top_3_indices = similarities[0].argsort()[-3:][::-1]

    #recommended_books = df.iloc[top_3_indices]['book_title'].tolist()
    recommended_books = df.iloc[top_3_indices][['book_title', 'author']].values.tolist()

    return recommended_books
