# WIDENNET Pipeline — Smart Contract Vulnerability Detection

> **MSc Computer Science (AI) Final Project** — University of Kerala, 2026  
> Based on: *"Smart Contract Vulnerability Detection Using Wide and Deep Neural Network"*  
> Osei, Ma & Huang — *Science of Computer Programming*, Vol. 238, 2024

---

## Overview

WIDENNET is a deep learning pipeline that automatically detects **reentrancy** and **timestamp dependence** vulnerabilities in Ethereum smart contracts — entirely at the bytecode level.

The pipeline takes raw Solidity source code or EVM bytecode, disassembles it into opcode sequences, embeds those sequences using Word2Vec (CBOW), and classifies them using a Wide & Deep neural network.

**Key results on real-world datasets:**
- ✅ **89% accuracy** and **98% precision** for reentrancy detection
- ✅ **70% accuracy** for timestamp dependence detection
- ✅ False positive rate below **4%** for reentrancy

---

## Pipeline Architecture

```
Raw Solidity / Bytecode
         │
    ┌────▼────┐
    │ Ingest  │  ← Ethereum mainnet, Etherscan API, CI/CD hooks, manual upload
    └────┬────┘
         │
    ┌────▼──────────┐
    │  Preprocess   │  ← Compile (py-solc-x) → Disassemble (evmdasm) → Normalise opcodes
    └────┬──────────┘
         │
    ┌────▼────┐
    │  Embed  │  ← Word2Vec (CBOW, 100-dim) opcode embeddings
    └────┬────┘
         │
    ┌────▼────────┐
    │   Infer     │  ← Wide & Deep Neural Network (WIDENNET)
    └────┬────────┘
         │
    ┌────▼──────────────┐
    │  Post-process     │  ← Risk classification → Reports → Alerts
    └────┬──────────────┘
         │
    ┌────▼──────────────────────┐
    │  Monitor & Retrain        │  ← Drift detection, feedback loop, auto-retrain
    └───────────────────────────┘
```

---

## Model Architecture

```
Opcode Sequence (length L)
         │
  Embedding Layer (Word2Vec, 100-dim)
         │
    ┌────┴────┐
    │         │
  WIDE      DEEP
  (Global   (Flatten → FC → ReLU)
  Avg Pool)
    │         │
    └────┬────┘
     Concatenate
         │
   Dense + Softmax
  [Vulnerable | Safe]
```

Two separate WIDENNET models are trained — one per vulnerability class — matching the paper's experimental setup.

---

## Repository Structure

```
widennet-pipeline/
├── api.py                  # REST API for vulnerability prediction
├── check.py                # Quick sanity-check script
├── create_sample_data.py   # Generate sample contract data for testing
├── dataset.py              # Dataset loading and preparation
├── encode.py               # Opcode encoding and vocabulary mapping
├── evaluate.py             # Model evaluation (accuracy, F1, precision, recall)
├── model.py                # WIDENNET architecture (Wide & Deep, Keras)
├── predict.py              # Inference script for single/batch contracts
├── preprocess.py           # Solidity → bytecode → opcode normalisation
├── train.py                # Model training entry point
├── train_word2vec.py       # Word2Vec (CBOW) embedding training
├── requirements.txt        # Python dependencies
├── data/                   # Dataset directory (see Dataset section below)
├── logs/                   # Training logs
└── results/                # Evaluation outputs and reports
```

---

## Opcode Normalisation

Following the paper, variant opcode families are collapsed to reduce vocabulary sparsity:

| Raw Opcode Family | Normalised Token |
|---|---|
| PUSH1 … PUSH32 | `PUSH` |
| DUP1 … DUP16 | `DUP` |
| SWAP1 … SWAP16 | `SWAP` |
| LOG0 … LOG4 | `LOG` |

---

## Decision Thresholds

Raw softmax probabilities are converted to binary predictions using tunable thresholds:

| Vulnerability | Default Threshold | Rationale |
|---|---|---|
| Reentrancy | 0.50 | High precision (0.98); false negatives are costly |
| Timestamp Dependence | 0.65 | Reduces FPR (~39% at 0.50) |

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- Git

### Install dependencies

```bash
git clone https://github.com/Deepu-p-123/widennet-pipeline.git
cd widennet-pipeline
pip install -r requirements.txt
```

---

## Dataset

This project uses the **IJCAI-2020 Smart Contract Dataset** (Qian et al., 2020).

📥 **Download the dataset** from the [Messi-Q GitHub repository](https://github.com/Messi-Q/Smart-Contract-Dataset) and place it in the `data/` directory:

```
data/
└── Smart-Contract-Dataset/
    ├── reentrancy/
    └── timestamp/
```

---

## Usage

### 1. Train Word2Vec embeddings
```bash
python train_word2vec.py
```

### 2. Train the WIDENNET model
```bash
python train.py
```

### 3. Evaluate the model
```bash
python evaluate.py
```

### 4. Predict on a contract
```bash
python predict.py --contract path/to/contract.sol
```

### 5. Run the API
```bash
python api.py
```

---

## Model Weights

Trained model files (`best_widennet.keras`, `widennet_final.keras`) are not stored in this repository due to GitHub's 100MB file size limit.

📥 **Download pre-trained models:** [Google Drive link — *coming soon*]

Place downloaded `.keras` files in the `models/` directory before running inference.

---

## Results

| Metric | Reentrancy | Timestamp Dependence |
|---|---|---|
| Accuracy | 89% | 70% |
| Precision | 98% | — |
| F1-Score | 0.92 | 0.70 |
| False Positive Rate | < 4% | ~39% (mitigated via threshold tuning) |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| ML Framework | TensorFlow 2.x / Keras |
| Embeddings | Gensim Word2Vec |
| Bytecode Processing | evmdasm, py-solc-x |
| API | FastAPI / Flask |
| Database | PostgreSQL, SQLite |
| Visualisation | Matplotlib, Seaborn |

---

## Research Reference

This project implements and extends the pipeline described in:

> Osei, S. B., Ma, Z., & Huang, R. (2024).  
> *Smart Contract Vulnerability Detection Using Wide and Deep Neural Network.*  
> Science of Computer Programming, Vol. 238, 103172.  
> [https://doi.org/10.1016/j.scico.2023.103172](https://doi.org/10.1016/j.scico.2023.103172)

---

## Author

**Deepu P**  
MSc Computer Science (Artificial Intelligence) — University of Kerala, 2026  
📧 pdeepuprakash@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/deepu-p) | [GitHub](https://github.com/Deepu-p-123) | [Portfolio](https://deepup-portfolio.netlify.app)

---

*Document version: 1.0 — May 2026*
