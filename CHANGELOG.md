# Changelog

All notable changes to WIDENNET will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-05-01

### Added
- Initial public release
- WIDENNET model architecture (Wide & Deep Neural Network, Keras/TensorFlow)
- Word2Vec CBOW opcode embedding training (`train_word2vec.py`)
- Full preprocessing pipeline: Solidity → bytecode → normalized opcodes
- Reentrancy vulnerability detection (89% accuracy, 98% precision)
- Timestamp dependence vulnerability detection (70% accuracy)
- Tunable decision thresholds (0.50 for reentrancy, 0.65 for timestamp)
- Opcode normalization: PUSH1–PUSH32 → PUSH, DUP1–DUP16 → DUP, etc.
- REST API for vulnerability prediction (FastAPI)
- Batch inference support
- Evaluation metrics: accuracy, precision, recall, F1, false positive rate
- GPL-3.0 license
- CITATION.cff for academic citation
- Unit tests for model architecture and inference

### Research Reference
Based on: Osei, Ma & Huang (2024), Science of Computer Programming, Vol. 238.
DOI: https://doi.org/10.1016/j.scico.2024.103172

---

## [Unreleased]

### Planned
- Support for additional vulnerability types (integer overflow, access control)
- Docker container for easy deployment
- Pre-trained model weights download via CLI
- Streamlit web demo
- ReadTheDocs full documentation
