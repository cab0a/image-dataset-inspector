"""Relative-behavior tests for the image metrics."""

import cv2
import numpy as np

from image_dataset_inspector.metrics import (
    calculate_blur_score,
    calculate_brightness,
    calculate_contrast,
)


def test_bright_image_has_higher_brightness() -> None:
    dark = np.full((64, 64, 3), 24, dtype=np.uint8)
    bright = np.full((64, 64, 3), 220, dtype=np.uint8)

    assert calculate_brightness(bright) > calculate_brightness(dark)


def test_high_contrast_image_has_higher_contrast() -> None:
    low_contrast = np.full((64, 64), 128, dtype=np.uint8)
    high_contrast = np.zeros((64, 64), dtype=np.uint8)
    high_contrast[:, 32:] = 255

    assert calculate_contrast(high_contrast) > calculate_contrast(low_contrast)


def test_sharp_image_has_higher_blur_score_than_blurred_image() -> None:
    row_indices, column_indices = np.indices((128, 128))
    sharp = (((row_indices // 8 + column_indices // 8) % 2) * 255).astype(
        np.uint8
    )
    blurred = cv2.GaussianBlur(sharp, (15, 15), 0)

    assert calculate_blur_score(sharp) > calculate_blur_score(blurred)
