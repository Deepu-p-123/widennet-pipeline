# Contributing to WIDENNET

Thank you for your interest in contributing!  
WIDENNET is open source under **GPL-3.0**. All contributions must be compatible with this license.

---

## Ways to Contribute

- Report bugs via [GitHub Issues](https://github.com/Deepu-p-123/widennet-pipeline/issues)
- Suggest new vulnerability detection types
- Improve model accuracy or add new architectures
- Improve documentation
- Add more unit tests

---

## Development Setup

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/widennet-pipeline.git
cd widennet-pipeline

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install in editable mode with dev dependencies
pip install -e ".[dev]"

# 4. Run tests to verify everything works
pytest tests/
```

---

## Pull Request Guidelines

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Write or update tests for your changes
3. Make sure all tests pass: `pytest tests/`
4. Format code: `black widennet/`
5. Submit a Pull Request with a clear description

---

## Code Style

- Follow PEP 8
- Use `black` for formatting (line length: 88)
- Add GPL-3.0 header to every new Python file (see existing files for the template)
- Add docstrings to all public functions

---

## Citing This Work

If you use WIDENNET in research, please cite both the software and the original paper.
See [CITATION.cff](CITATION.cff) for the correct citation format.

---

## License

By contributing, you agree that your contributions will be licensed under GPL-3.0.
