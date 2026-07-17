"""Tests for directory inspection and CSV reporting."""

import csv
from pathlib import Path

from image_dataset_inspector.inspector import inspect_directory
from image_dataset_inspector.reporting import CSV_COLUMNS, write_csv_report


def test_valid_image_is_read_recursively(synthetic_dataset: Path) -> None:
    results = inspect_directory(synthetic_dataset)
    valid = next(result for result in results if result.status == "valid")

    assert valid.relative_path == "nested/valid.png"
    assert valid.file_size_bytes is not None
    assert valid.width == 48
    assert valid.height == 32
    assert valid.channels == 3
    assert valid.brightness is not None
    assert valid.contrast is not None
    assert valid.blur_score is not None
    assert valid.error_message == ""


def test_corrupted_image_is_recorded_as_unreadable(
    synthetic_dataset: Path,
) -> None:
    results = inspect_directory(synthetic_dataset)
    unreadable = next(result for result in results if result.status == "unreadable")

    assert unreadable.relative_path == "broken.jpg"
    assert unreadable.file_size_bytes is not None
    assert unreadable.width is None
    assert unreadable.error_message == "OpenCV could not decode the image."


def test_csv_report_is_generated(synthetic_dataset: Path, tmp_path: Path) -> None:
    results = inspect_directory(synthetic_dataset)
    report_path = tmp_path / "reports" / "report.csv"

    write_csv_report(results, report_path)

    assert report_path.is_file()
    with report_path.open(encoding="utf-8", newline="") as report_file:
        reader = csv.DictReader(report_file)
        rows = list(reader)

    assert tuple(reader.fieldnames or ()) == CSV_COLUMNS
    assert len(rows) == 2
    assert {row["status"] for row in rows} == {"valid", "unreadable"}
