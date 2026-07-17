"""Download freely reusable images and generate an inspection example."""

from __future__ import annotations

import argparse
import hashlib
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from image_dataset_inspector.inspector import InspectionResult, inspect_directory
from image_dataset_inspector.reporting import write_csv_report


@dataclass(frozen=True, slots=True)
class PublicSample:
    """Metadata for one pinned, freely reusable sample image."""

    filename: str
    url: str
    sha256: str


BASE_URL = (
    "https://raw.githubusercontent.com/scikit-image/scikit-image/"
    "v0.26.0/src/skimage/data"
)
SAMPLES = (
    PublicSample(
        "camera.png",
        f"{BASE_URL}/camera.png",
        "b0793d2adda0fa6ae899c03989482bff9a42d3d5690fc7e3648f2795d730c23a",
    ),
    PublicSample(
        "coffee.png",
        f"{BASE_URL}/coffee.png",
        "cc02f8ca188b167c775a7101b5d767d1e71792cf762c33d6fa15a4599b5a8de7",
    ),
    PublicSample(
        "clock_motion.png",
        f"{BASE_URL}/clock_motion.png",
        "f029226b28b642e80113d86622e9b215ee067a0966feaf5e60604a1e05733955",
    ),
    PublicSample(
        "rocket.jpg",
        f"{BASE_URL}/rocket.jpg",
        "c2dd0de7c538df8d111e479619b129464d0269d0ae5fd18ca91d33a7fdfea95c",
    ),
    PublicSample(
        "hubble_deep_field.jpg",
        f"{BASE_URL}/hubble_deep_field.jpg",
        "3a19c5dd8a927a9334bb1229a6d63711b1c0c767fb27e2286e7c84a3e2c2f5f4",
    ),
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download_samples(images_dir: Path) -> None:
    """Download all pinned sample images and verify their SHA-256 hashes."""
    images_dir.mkdir(parents=True, exist_ok=True)
    for sample in SAMPLES:
        destination = images_dir / sample.filename
        if (
            destination.is_file()
            and _sha256(destination.read_bytes()) == sample.sha256
        ):
            continue

        request = urllib.request.Request(
            sample.url,
            headers={"User-Agent": "image-dataset-inspector-public-sample"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
        if _sha256(data) != sample.sha256:
            raise ValueError(f"Checksum verification failed for {sample.filename}.")
        destination.write_bytes(data)


def _fit_thumbnail(
    image: np.ndarray,
    width: int = 360,
    height: int = 240,
) -> np.ndarray:
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(
        image,
        (
            max(1, round(image.shape[1] * scale)),
            max(1, round(image.shape[0] * scale)),
        ),
        interpolation=cv2.INTER_AREA,
    )
    canvas = np.full((height, width, 3), 24, dtype=np.uint8)
    y_offset = (height - resized.shape[0]) // 2
    x_offset = (width - resized.shape[1]) // 2
    canvas[
        y_offset : y_offset + resized.shape[0],
        x_offset : x_offset + resized.shape[1],
    ] = resized
    return canvas


def _create_panel(
    image_path: Path,
    result: InspectionResult,
) -> np.ndarray:
    image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise OSError(f"Could not read downloaded sample: {image_path}")

    thumbnail = _fit_thumbnail(image)
    panel = cv2.copyMakeBorder(
        thumbnail,
        56,
        0,
        0,
        0,
        cv2.BORDER_CONSTANT,
        value=(24, 24, 24),
    )
    cv2.putText(
        panel,
        result.relative_path,
        (8, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    metrics_text = (
        f"brightness={result.brightness:.1f}  "
        f"contrast={result.contrast:.1f}  "
        f"blur={result.blur_score:.1f}"
    )
    cv2.putText(
        panel,
        metrics_text,
        (8, 43),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (210, 210, 210),
        1,
        cv2.LINE_AA,
    )
    return panel


def create_contact_sheet(
    images_dir: Path,
    results: list[InspectionResult],
    output_path: Path,
) -> None:
    """Create a compact visual index of the downloaded images and metrics."""
    panels = [
        _create_panel(images_dir / result.relative_path, result)
        for result in results
        if result.status == "valid"
    ]
    if not panels:
        raise ValueError("The contact sheet requires at least one valid image.")
    blank_panel = np.full_like(panels[0], 24)
    if len(panels) % 2:
        panels.append(blank_panel)
    rows = [
        cv2.hconcat(panels[index : index + 2])
        for index in range(0, len(panels), 2)
    ]
    if not cv2.imwrite(str(output_path), cv2.vconcat(rows)):
        raise OSError(f"Could not write contact sheet: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    """Create the public-sample command-line parser."""
    parser = argparse.ArgumentParser(
        description="Inspect a pinned set of freely reusable sample images."
    )
    parser.add_argument(
        "--images",
        type=Path,
        default=Path("examples/public_sample/images"),
        help="Directory used to cache downloaded sample images.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("examples/public_sample"),
        help="Directory for the CSV report and contact sheet.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Download, inspect, and summarize the public sample images."""
    args = build_parser().parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    download_samples(args.images)
    results = inspect_directory(args.images)

    report_path = args.output / "public_sample_report.csv"
    contact_sheet_path = args.output / "public_sample_contact_sheet.jpg"
    write_csv_report(results, report_path)
    create_contact_sheet(args.images, results, contact_sheet_path)

    valid_count = sum(result.status == "valid" for result in results)
    print(f"Images: {len(results)}")
    print(f"Valid: {valid_count}")
    print(f"Report: {report_path}")
    print(f"Contact sheet: {contact_sheet_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
