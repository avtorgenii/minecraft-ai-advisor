from encoder import load_st
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained model
model = load_st()

# Example chunks (your webpage parts)
documents = []

# Generate embeddings for documents and query
doc_embeddings = model.encode(documents)
query = "where to diamond pickaxe in minecraft"
query_embedding = model.encode([query])

# Calculate cosine similarity between query and document embeddings
similarities = cosine_similarity(query_embedding, doc_embeddings)

# Retrieve the most relevant document (chunk)
most_relevant_doc_index = similarities.argmax()
print(documents[most_relevant_doc_index])
