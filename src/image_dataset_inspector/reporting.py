"""CSV report generation."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

from image_dataset_inspector.inspector import InspectionResult

CSV_COLUMNS = (
    "relative_path",
    "file_size_bytes",
    "width",
    "height",
    "channels",
    "brightness",
    "contrast",
    "blur_score",
    "status",
    "error_message",
)


def _format_metric(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}"


def _to_row(result: InspectionResult) -> dict[str, object]:
    return {
        "relative_path": result.relative_path,
        "file_size_bytes": "" if result.file_size_bytes is None else result.file_size_bytes,
        "width": "" if result.width is None else result.width,
        "height": "" if result.height is None else result.height,
        "channels": "" if result.channels is None else result.channels,
        "brightness": _format_metric(result.brightness),
        "contrast": _format_metric(result.contrast),
        "blur_score": _format_metric(result.blur_score),
        "status": result.status,
        "error_message": result.error_message,
    }


def write_csv_report(results: Iterable[InspectionResult], output_path: Path) -> None:
    """Write inspection results to a UTF-8 CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as report_file:
        writer = csv.DictWriter(
            report_file,
            fieldnames=CSV_COLUMNS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(_to_row(result) for result in results)
