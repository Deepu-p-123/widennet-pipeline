import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from model import build_widennet

X = np.load("data/X.npy")
y = np.load("data/y.npy")
emb_matrix = np.load("models/embedding_matrix.npy")

# 80/20 stratified split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Class weights for imbalanced data
classes = np.unique(y_train)
weights = compute_class_weight("balanced", classes=classes,
                                y=y_train)
class_weights = dict(zip(classes, weights))
print("Class weights:", class_weights)

vocab_size = emb_matrix.shape[0]
model = build_widennet(vocab_size, 100, 512, emb_matrix)

callbacks = [
    EarlyStopping(monitor="val_loss", patience=10,
                  restore_best_weights=True, verbose=1),
    ModelCheckpoint("models/best_widennet.keras",
                    save_best_only=True, monitor="val_loss")
]

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=32,
    class_weight=class_weights,
    callbacks=callbacks,
    verbose=1
)

model.save("models/widennet_final.keras")
print("Training complete.")