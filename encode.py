import pickle, json
import numpy as np
from gensim.models import Word2Vec
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 512     # fixed sequence length (tune this)
EMB_DIM = 100

w2v = Word2Vec.load("models/word2vec_opcodes.model")

# Build vocab index: 0 = PAD, 1 = UNK
vocab = list(w2v.wv.index_to_key)
word_index = {op: i+2 for i, op in enumerate(vocab)}
word_index["<PAD>"] = 0
word_index["<UNK>"] = 1

with open("models/vocab_index.json", "w") as f:
    json.dump(word_index, f)

# Build embedding matrix (rows = vocab, cols = 100-dim vector)
emb_matrix = np.zeros((len(word_index), EMB_DIM))
for op, idx in word_index.items():
    if op in w2v.wv:
        emb_matrix[idx] = w2v.wv[op]

np.save("models/embedding_matrix.npy", emb_matrix)

# Encode the dataset
with open("data/opcode_seqs.pkl", "rb") as f:
    data = pickle.load(f)

encoded = [[word_index.get(op, 1) for op in seq]
           for seq in data["opcodes"]]

X = pad_sequences(encoded, maxlen=MAX_LEN, padding="post",
                  truncating="post", value=0)
y = np.array(data["labels"])

np.save("data/X.npy", X)
np.save("data/y.npy", y)
print(f"X shape: {X.shape} | y shape: {y.shape}")