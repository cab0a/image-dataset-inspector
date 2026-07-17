"""Recursive JPEG and PNG inspection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2

from image_dataset_inspector.metrics import (
    calculate_blur_score,
    calculate_brightness,
    calculate_contrast,
)

SUPPORTED_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png"})


@dataclass(frozen=True, slots=True)
class InspectionResult:
    """Inspection data for one image candidate."""

    relative_path: str
    file_size_bytes: int | None
    width: int | None
    height: int | None
    channels: int | None
    brightness: float | None
    contrast: float | None
    blur_score: float | None
    status: str
    error_message: str


def find_image_paths(root: Path) -> list[Path]:
    """Return supported image paths below root in deterministic order."""
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def inspect_image(path: Path, root: Path) -> InspectionResult:
    """Inspect one image without propagating per-file read failures."""
    relative_path = path.relative_to(root).as_posix()

    try:
        file_size = path.stat().st_size
    except OSError:
        return InspectionResult(
            relative_path=relative_path,
            file_size_bytes=None,
            width=None,
            height=None,
            channels=None,
            brightness=None,
            contrast=None,
            blur_score=None,
            status="unreadable",
            error_message="Could not read file metadata.",
        )

    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None or image.size == 0:
        return InspectionResult(
            relative_path=relative_path,
            file_size_bytes=file_size,
            width=None,
            height=None,
            channels=None,
            brightness=None,
            contrast=None,
            blur_score=None,
            status="unreadable",
            error_message="OpenCV could not decode the image.",
        )

    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else int(image.shape[2])

    try:
        brightness = calculate_brightness(image)
        contrast = calculate_contrast(image)
        blur_score = calculate_blur_score(image)
    except (cv2.error, ValueError, TypeError):
        return InspectionResult(
            relative_path=relative_path,
            file_size_bytes=file_size,
            width=int(width),
            height=int(height),
            channels=channels,
            brightness=None,
            contrast=None,
            blur_score=None,
            status="unreadable",
            error_message="The image was decoded, but its metrics could not be calculated.",
        )

    return InspectionResult(
        relative_path=relative_path,
        file_size_bytes=file_size,
        width=int(width),
        height=int(height),
        channels=channels,
        brightness=brightness,
        contrast=contrast,
        blur_score=blur_score,
        status="valid",
        error_message="",
    )


def inspect_directory(root: Path) -> list[InspectionResult]:
    """Inspect all supported images below a directory."""
    if not root.is_dir():
        raise NotADirectoryError("The input path must be a directory.")
    return [inspect_image(path, root) for path in find_image_paths(root)]
