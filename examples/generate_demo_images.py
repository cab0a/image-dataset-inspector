"""Generate a small synthetic dataset for the command-line demo."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray


def _write_image(path: Path, image: NDArray[np.generic]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise RuntimeError(f"Could not create demo image: {path}")


def generate_demo_images(output_dir: Path) -> int:
    """Create valid images with varied properties and one invalid JPEG."""
    output_dir.mkdir(parents=True, exist_ok=True)

    dark = np.full((128, 128, 3), 32, dtype=np.uint8)
    bright = np.full((128, 128, 3), 224, dtype=np.uint8)

    row_indices, column_indices = np.indices((128, 128))
    checkerboard = (
        ((row_indices // 8 + column_indices // 8) % 2) * 255
    ).astype(np.uint8)
    blurred_checkerboard = cv2.GaussianBlur(checkerboard, (15, 15), 0)

    gradient = np.tile(
        np.linspace(0, 255, 128, dtype=np.uint8),
        (128, 1),
    )
    color_gradient = cv2.merge((gradient, np.flipud(gradient), gradient))

    _write_image(output_dir / "dark.png", dark)
    _write_image(output_dir / "bright.png", bright)
    _write_image(output_dir / "checkerboard.png", checkerboard)
    _write_image(output_dir / "blurred_checkerboard.jpg", blurred_checkerboard)
    _write_image(output_dir / "nested" / "color_gradient.png", color_gradient)
    (output_dir / "broken.jpg").write_bytes(b"This is not a valid JPEG file.\n")

    return 6


def main() -> int:
    """Parse arguments and generate the demo dataset."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("demo_images"),
        help="Directory for generated images (default: demo_images).",
    )
    args = parser.parse_args()

    created_count = generate_demo_images(args.output)
    print(f"Created: {created_count}")
    print(f"Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
