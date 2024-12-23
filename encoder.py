from sentence_transformers import SentenceTransformer

def save_st(verbose=False):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.save_pretrained("./model")

    if verbose:
        print("Saved model to disk")

def load_st(verbose=False):
    model = SentenceTransformer('./model')

    if verbose:
        print("Loaded model")

    return model
