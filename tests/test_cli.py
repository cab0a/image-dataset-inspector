"""Tests for command-line exit codes."""

from pathlib import Path

import pytest

from image_dataset_inspector.cli import main


def test_missing_input_directory_returns_exit_code_2(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report_path = tmp_path / "report.csv"

    exit_code = main(
        ["inspect", str(tmp_path / "missing"), "--output", str(report_path)]
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert "input path must be a readable directory" in captured.err
    assert not report_path.exists()


def test_unwritable_output_returns_exit_code_1(
    synthetic_dataset: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_directory = tmp_path / "existing-directory"
    output_directory.mkdir()

    exit_code = main(
        [
            "inspect",
            str(synthetic_dataset),
            "--output",
            str(output_directory),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "CSV report could not be written" in captured.err
