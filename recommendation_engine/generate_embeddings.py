import csv
import numpy as np
import pandas as pd
import torch
from transformers import BertTokenizer, BertModel

# Using pre-trained BERT model and tokenizer
# Not using OpenAI's embedding here because they have a token limit per minute. The OpenAI's APIs are unable to process this dataset.
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
data = []

with open('data/booksummaries.txt', 'r') as f:
    reader = csv.reader(f, dialect='excel-tab')
    for row in reader:
        data.append(row)
df_full = pd.DataFrame.from_records(data, columns=['book_id', 'freebase_id', 'book_title', 'author', 'publication_date', 'genre', 'summary'])
# Processing the whole dataset is taking way too many resources and long time. Hence, only using a subset of the dataset
df = df_full.head(1000)

book_tokens = tokenizer(df['summary'].tolist(), return_tensors="pt", padding=True, truncation=True)
with torch.no_grad():
    book_embeddings = model(**book_tokens).last_hidden_state.mean(dim=1).numpy()
np.save('book_embeddings.npy', book_embeddings)