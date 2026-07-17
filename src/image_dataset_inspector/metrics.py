"""Simple image metrics used by the dataset inspector."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray


def to_grayscale(image: NDArray[np.generic]) -> NDArray[np.generic]:
    """Convert an OpenCV image to a single grayscale channel."""
    if image.ndim == 2:
        return image
    if image.ndim != 3:
        raise ValueError("The decoded image must have two or three dimensions.")

    channels = image.shape[2]
    if channels == 1:
        return image[:, :, 0]
    if channels == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if channels == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    raise ValueError("The decoded image has an unsupported channel count.")


def calculate_brightness(image: NDArray[np.generic]) -> float:
    """Return the mean grayscale intensity."""
    grayscale = to_grayscale(image)
    return float(np.mean(grayscale))


def calculate_contrast(image: NDArray[np.generic]) -> float:
    """Return the standard deviation of grayscale intensities."""
    grayscale = to_grayscale(image)
    return float(np.std(grayscale))


def calculate_blur_score(image: NDArray[np.generic]) -> float:
    """Return the variance of the grayscale Laplacian."""
    grayscale = to_grayscale(image)
    laplacian = cv2.Laplacian(grayscale, cv2.CV_64F)
    return float(np.var(laplacian))
