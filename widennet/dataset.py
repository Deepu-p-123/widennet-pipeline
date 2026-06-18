import pandas as pd
import pickle
from preprocess import preprocess_contract

# CSV columns expected: 'source_code', 'label', 'solc_version'
df = pd.read_csv("data/contracts.csv")

opcode_seqs = []
labels      = []
skipped     = 0

for _, row in df.iterrows():
    try:
        opcodes = preprocess_contract(
            row["source_code"],
            version=str(row.get("solc_version", "0.8.0"))
        )
        if len(opcodes) < 10:
            skipped += 1
            continue
        opcode_seqs.append(opcodes)
        labels.append(int(row["label"]))
    except Exception as e:
        skipped += 1

print(f"Processed: {len(opcode_seqs)} | Skipped: {skipped}")

with open("data/opcode_seqs.pkl", "wb") as f:
    pickle.dump({"opcodes": opcode_seqs, "labels": labels}, f)
print("Saved to data/opcode_seqs.pkl")