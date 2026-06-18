# tests/test_model.py
#
# WIDENNET — Smart Contract Vulnerability Detection
# Copyright (C) 2026  Deepu P <pdeepuprakash@gmail.com>
# License: GNU General Public License v3.0

"""
Unit tests for the WIDENNET model architecture.
Run with: pytest tests/
"""

import numpy as np
import pytest


class TestBuildWidennet:
    """Tests for the build_widennet() function."""

    @pytest.fixture
    def dummy_embedding_matrix(self):
        """Create a small dummy embedding matrix for testing."""
        vocab_size = 100
        emb_dim = 100
        return np.random.rand(vocab_size, emb_dim).astype(np.float32)

    def test_model_builds_without_error(self, dummy_embedding_matrix):
        """Model should build with valid inputs."""
        from widennet.model import build_widennet
        vocab_size = dummy_embedding_matrix.shape[0]
        model = build_widennet(
            vocab_size=vocab_size,
            emb_dim=100,
            max_len=512,
            emb_matrix=dummy_embedding_matrix,
            num_classes=2
        )
        assert model is not None

    def test_model_output_shape(self, dummy_embedding_matrix):
        """Model output should match num_classes."""
        from widennet.model import build_widennet
        vocab_size = dummy_embedding_matrix.shape[0]
        model = build_widennet(
            vocab_size=vocab_size,
            emb_dim=100,
            max_len=512,
            emb_matrix=dummy_embedding_matrix,
            num_classes=2
        )
        # Output layer should have 2 units (Vulnerable / Safe)
        assert model.output_shape == (None, 2)

    def test_model_has_wide_and_deep_paths(self, dummy_embedding_matrix):
        """Model should contain both wide and deep named layers."""
        from widennet.model import build_widennet
        vocab_size = dummy_embedding_matrix.shape[0]
        model = build_widennet(
            vocab_size=vocab_size,
            emb_dim=100,
            max_len=512,
            emb_matrix=dummy_embedding_matrix,
        )
        layer_names = [layer.name for layer in model.layers]
        assert "wide_gap" in layer_names, "Wide path (GlobalAveragePooling) missing"
        assert "deep_flatten" in layer_names, "Deep path (Flatten) missing"
        assert "concat" in layer_names, "Concatenation layer missing"

    def test_model_inference_shape(self, dummy_embedding_matrix):
        """Model should produce correct output shape on dummy input."""
        from widennet.model import build_widennet
        vocab_size = dummy_embedding_matrix.shape[0]
        model = build_widennet(
            vocab_size=vocab_size,
            emb_dim=100,
            max_len=32,
            emb_matrix=dummy_embedding_matrix,
        )
        # Single sample, sequence length 32
        dummy_input = np.zeros((1, 32), dtype=np.int32)
        output = model.predict(dummy_input, verbose=0)
        assert output.shape == (1, 2)

    def test_output_is_probability_distribution(self, dummy_embedding_matrix):
        """Softmax output should sum to 1.0 per sample."""
        from widennet.model import build_widennet
        vocab_size = dummy_embedding_matrix.shape[0]
        model = build_widennet(
            vocab_size=vocab_size,
            emb_dim=100,
            max_len=32,
            emb_matrix=dummy_embedding_matrix,
        )
        dummy_input = np.zeros((4, 32), dtype=np.int32)
        output = model.predict(dummy_input, verbose=0)
        sums = output.sum(axis=1)
        np.testing.assert_allclose(sums, np.ones(4), atol=1e-5)


class TestModelVersion:
    """Test that the package version is correctly set."""

    def test_version_exists(self):
        import widennet
        assert hasattr(widennet, "__version__")

    def test_version_format(self):
        import widennet
        parts = widennet.__version__.split(".")
        assert len(parts) == 3, "Version should follow MAJOR.MINOR.PATCH format"
