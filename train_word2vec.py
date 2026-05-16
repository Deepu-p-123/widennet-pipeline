import pickle
from gensim.models import Word2Vec

with open("data/opcode_seqs.pkl", "rb") as f:
    data = pickle.load(f)

opcode_seqs = data["opcodes"]

model = Word2Vec(
    sentences=opcode_seqs,
    vector_size=100,      # embedding dimensions
    window=5,             # context window
    min_count=1,          # keep all opcodes
    sg=0,                 # sg=0 → CBOW (paper uses CBOW)
    epochs=10,
    workers=4
)

model.save("models/word2vec_opcodes.model")
print(f"Vocab size: {len(model.wv)}")
print(f"Sample vector for PUSH: {model.wv['PUSH'][:5]}")