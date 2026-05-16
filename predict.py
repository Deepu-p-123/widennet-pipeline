import json, numpy as np, tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from preprocess import preprocess_contract

MAX_LEN = 512
THRESHOLD_REENTRANCY  = 0.50   # paper: high precision
THRESHOLD_TIMESTAMP   = 0.65   # raised to cut FPR

model      = tf.keras.models.load_model("models/widennet_final.keras")
vocab_idx  = json.load(open("models/vocab_index.json"))

def predict_contract(sol_source: str,
                     solc_version: str = "0.8.0") -> dict:
    opcodes = preprocess_contract(sol_source, solc_version)
    encoded = [vocab_idx.get(op, 1) for op in opcodes]
    X       = pad_sequences([encoded], maxlen=MAX_LEN,
                             padding="post", truncating="post")

    probs   = model.predict(X, verbose=0)[0]
    vuln_score = float(probs[1])   # probability of vulnerable

    return {
        "vulnerable":   vuln_score >= THRESHOLD_REENTRANCY,
        "score":        round(vuln_score, 4),
        "risk":         "CRITICAL" if vuln_score >= 0.90
                        else "HIGH" if vuln_score >= 0.50
                        else "LOW",
        "opcodes_used": len(opcodes)
    }

if __name__ == "__main__":
    sample = open("data/sample.sol").read()
    result = predict_contract(sample)
    print(result)