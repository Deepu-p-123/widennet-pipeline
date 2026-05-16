import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model

def build_widennet(vocab_size, emb_dim, max_len,
                   emb_matrix, num_classes=2):
    inp = layers.Input(shape=(max_len,), name="opcode_input")

    # Shared embedding (Word2Vec weights, trainable)
    emb = layers.Embedding(
        input_dim=vocab_size,
        output_dim=emb_dim,
        weights=[emb_matrix],
        trainable=True,         # fine-tune during training
        name="embedding"
    )(inp)

    # ── WIDE path: memorisation ──────────────────────────
    wide = layers.GlobalAveragePooling1D(name="wide_gap")(emb)
    wide = layers.BatchNormalization()(wide)

    # ── DEEP path: generalisation ────────────────────────
    deep = layers.Flatten(name="deep_flatten")(emb)
    deep = layers.Dense(192, activation="relu")(deep)
    deep = layers.Dropout(0.3)(deep)
    deep = layers.Dense(320, activation="relu")(deep)
    deep = layers.Dropout(0.3)(deep)

    # ── Fusion ───────────────────────────────────────────
    fused = layers.Concatenate(name="concat")([wide, deep])
    out   = layers.Dense(num_classes,
                         activation="softmax",
                         name="output")(fused)

    model = Model(inputs=inp, outputs=out, name="WIDENNET")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

if __name__ == "__main__":
    emb_matrix = np.load("models/embedding_matrix.npy")
    vocab_size  = emb_matrix.shape[0]
    m = build_widennet(vocab_size, 100, 512, emb_matrix)
    m.summary()