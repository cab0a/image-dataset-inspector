"""Synthetic pytest fixtures for image inspection."""

from pathlib import Path

import cv2
import numpy as np
import pytest


@pytest.fixture
def synthetic_dataset(tmp_path: Path) -> Path:
    """Create one valid image, one invalid image, and one ignored file."""
    dataset = tmp_path / "images"
    nested = dataset / "nested"
    nested.mkdir(parents=True)

    valid_image = np.full((32, 48, 3), 120, dtype=np.uint8)
    assert cv2.imwrite(str(nested / "valid.png"), valid_image)
    (dataset / "broken.jpg").write_bytes(b"invalid image data")
    (dataset / "notes.txt").write_text("not an image", encoding="utf-8")
    return dataset
