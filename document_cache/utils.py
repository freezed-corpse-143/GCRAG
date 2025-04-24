from sentence_transformers import SentenceTransformer

encode_model = SentenceTransformer('FacebookAI/roberta-base')

def text_encoder(text):
    return encode_model.encode(sentences)