from rank_bm25 import BM25Okapi
import re

bm25_index = None
bm25_chunks=[]

def build_bm25_index(chunks):
    global bm25_index, bm25_chunks

    # tokenized = [chunk["code"].split() for chunk in chunks]
    tokenized = [re.findall(r'\w+', chunk["code"].lower()) for chunk in chunks]

    bm25_index = BM25Okapi(tokenized)
    bm25_chunks = chunks



def search_bm25(question, top_n=3):
    # tokenized_query = question.split()
    tokenized_query = re.findall(r'\w+', question.lower())
    scores = bm25_index.get_scores(tokenized_query)

    top_indices = sorted(range(len(scores)), key=lambda i:scores[i], reverse=True)[:top_n]

    results = [bm25_chunks[i] for i in top_indices]

    return results