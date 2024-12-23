from sentence_transformers import SentenceTransformer

def save_st(verbose=False):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.save_pretrained("./model")

    if verbose:
        print("Saved model to disk")

    return model

def load_st(verbose=False):
    try:
        model = SentenceTransformer('./model')
        return model
    except Exception as e:
        print(e)
        return save_st(verbose=verbose)




if __name__ == '__main__':
    load_st(verbose=True)