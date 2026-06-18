import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score)
from sklearn.model_selection import train_test_split

X = np.load("data/X.npy")
y = np.load("data/y.npy")
_, X_val, _, y_val = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = tf.keras.models.load_model("models/widennet_final.keras")

probs   = model.predict(X_val)
y_pred  = np.argmax(probs, axis=1)

print(classification_report(y_val, y_pred,
      target_names=["Not Vulnerable", "Vulnerable"]))

cm = confusion_matrix(y_val, y_pred)
tn, fp, fn, tp = cm.ravel()
fpr = fp / (fp + tn)
fnr = fn / (fn + tp)
print(f"FPR: {fpr:.3f}  |  FNR: {fnr:.3f}")

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Not Vuln", "Vuln"],
            yticklabels=["Not Vuln", "Vuln"])
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("results/confusion_matrix.png", dpi=150)
print("Saved confusion_matrix.png")