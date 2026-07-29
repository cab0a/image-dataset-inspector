# Image Dataset Inspector

## 日本語概要

このリポジトリは、JPEG・PNGフォルダを再帰的に検査し、画像の縦横寸法、ファイル容量、明るさ、コントラスト、ラプラシアン分散、読み込みエラーをCSVへ出力するPython製コマンドラインツールです。

壊れた画像があっても検査を継続し、入力が同じなら変化しない行順、合成テストデータ、チェックサム付きの公開サンプルを備えています。

Python 3.10〜3.14でテストを自動実行しています。指標の意味と制約は、以下の英語本文を参照してください。

---

[![CI](https://github.com/cab0a/image-dataset-inspector/actions/workflows/ci.yml/badge.svg)](https://github.com/cab0a/image-dataset-inspector/actions/workflows/ci.yml)

Audit JPEG and PNG folders from the command line without allowing one broken
image to hide the rest of the dataset.

## Overview

Image Dataset Inspector is a small Python command-line tool that recursively scans JPEG and PNG files, verifies that OpenCV can decode them, calculates simple image statistics, and writes a CSV inventory.

The project focuses on a narrow, reproducible workflow suitable for early dataset checks. It continues scanning when an individual file cannot be read and records the failure in the report.

This repository inspects inputs; it does not compare vision algorithms like
`vision-playground` or maintain a sequence of research studies like
`research-notes`.

## Problem

Image datasets often contain a mixture of valid images, corrupted files, inconsistent dimensions, and files with different visual characteristics. Discovering these issues before model training or image-processing experiments makes later failures easier to diagnose.

This tool provides a deterministic first-pass inventory without attempting to decide whether an image is suitable for a specific model or application.

## Representative Result

The public sample shows five checksum-verified CC0 or public-domain images
alongside the dimensions, brightness, contrast, and Laplacian-variance values
recorded in the generated CSV.

![Public image inspection sample](examples/public_sample/public_sample_contact_sheet.jpg)

Review the complete
[`public_sample_report.csv`](examples/public_sample/public_sample_report.csv)
for machine-readable values. The sample demonstrates that the metrics describe
content and scale; they are not universal image-quality scores.

## Key Features

- Recursively discovers `.jpg`, `.jpeg`, and `.png` files
- Records paths relative to the inspected directory
- Reports file size, dimensions, and channel count
- Calculates brightness, contrast, and a simple blur score
- Records unreadable images without stopping the scan
- Writes a UTF-8 CSV report
- Prints scanned, valid, and unreadable file counts
- Includes a fully synthetic demo dataset and unit tests

## Quick Start

Python 3.10 or later is required.

On Debian or Ubuntu, install the distribution-provided `python3-venv` package if `venv` reports that `ensurepip` is unavailable.

```bash
git clone https://github.com/cab0a/image-dataset-inspector.git
cd image-dataset-inspector
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python examples/generate_demo_images.py --output output/demo_images
image-dataset-inspector inspect output/demo_images \
  --output output/report.csv
```

Expected CLI summary:

```text
Scanned: 6
Valid: 5
Unreadable: 1
Report: output/report.csv
```

Review `output/report.csv`; it contains one row per discovered file, including the
deliberately unreadable `broken.jpg`.

## Generated Artifacts

- `output/report.csv` is a deterministic UTF-8 inventory with relative paths,
  dimensions, channel counts, descriptive metrics, status, and decode errors.
- `examples/public_sample/public_sample_report.csv` and
  `public_sample_contact_sheet.jpg` provide a reproducible real-image example.
- `output/demo_images/` is generated locally and includes five decodable images plus
  one corrupted JPEG for the failure-path demonstration.

## Usage

```text
image-dataset-inspector inspect INPUT_DIRECTORY --output REPORT.csv
```

Example:

```bash
image-dataset-inspector inspect ./images --output report.csv
```

The scan completes and writes a report even when individual files are unreadable. An invalid input directory or an unwritable report destination returns a non-zero exit code.

| Exit code | Meaning |
| ---: | --- |
| `0` | Scan completed and the CSV report was written; unreadable images may still be present as report rows |
| `1` | The CSV report could not be written |
| `2` | The input path was not a readable directory |

## Evaluation Methodology

The synthetic fixture provides known relative relationships and an explicit
decode failure. The public sample provides varied, traceable image content
without semantic quality labels. Together they test inventory behavior and
metric interpretation without presenting the descriptive statistics as an
acceptance threshold.

## Results: Public Image Sample

A reproducible real-image example downloads five CC0 or public-domain photographs from the scikit-image sample data, verifies their SHA-256 hashes, and generates a CSV report and contact sheet.

```bash
python examples/run_public_sample.py
```

The sample demonstrates that the metrics describe image content rather than absolute quality. In particular, dark images can still contain strong local detail, and Laplacian variance is influenced by texture, noise, scale, and blur. See the [public sample analysis and attribution](examples/public_sample/README.md) for the results, interpretation, and image licenses.

## Downstream Workflow

The CSV report can be used as an explicit input gate before a computer vision experiment. The [Vision Playground inspected public sample](https://github.com/cab0a/vision-playground/tree/main/results/inspected_public_sample) demonstrates this sequence:

`Input Inspection → Thresholding Prototype → Qualitative Evaluation → Interpretation`

Unreadable files remain visible in the input report, while only valid images continue to the experiment. The downstream workflow joins inspection metrics with thresholding outputs so assumptions and observed behavior can be reviewed together.

## Technical Design

### Output Schema

| Column | Description |
| --- | --- |
| `relative_path` | POSIX-style path relative to the inspected directory |
| `file_size_bytes` | File size in bytes |
| `width` | Decoded image width in pixels |
| `height` | Decoded image height in pixels |
| `channels` | Number of decoded image channels |
| `brightness` | Mean grayscale intensity |
| `contrast` | Standard deviation of grayscale intensities |
| `blur_score` | Variance of the grayscale Laplacian |
| `status` | `valid` or `unreadable` |
| `error_message` | Readable explanation when inspection fails |

Unavailable values are written as empty CSV fields. Metric values are written with six decimal places.

### Scan and Metric Methodology

OpenCV loads each image with unchanged channel information. A two-dimensional image is treated as one channel; three- and four-channel images are converted from BGR or BGRA to grayscale before metric calculation.

The metrics use intentionally simple definitions:

- **Brightness:** arithmetic mean of the grayscale image
- **Contrast:** standard deviation of the grayscale image
- **Blur score:** variance of the Laplacian of the grayscale image

The scanner sorts candidate paths before inspection so repeated runs over unchanged files produce a stable row order.

## Development and Testing

```bash
python -m pip install ".[dev]"
python -m pytest
```

The unit tests use images generated in temporary directories. They verify that:

- A valid image in a nested directory is decoded and measured
- A corrupted JPEG is recorded as unreadable
- A bright image has higher brightness than a dark image
- A high-contrast image has higher contrast than a uniform image
- A sharp checkerboard has a higher blur score than its blurred version
- A CSV report is created with both valid and unreadable rows
- Invalid input and unwritable output paths return documented error exit codes

These tests check relative metric behavior rather than fixed values that could be brittle across image-processing library versions.

GitHub Actions installs the project, verifies the CLI entry point, and runs the test suite on Python 3.10 through 3.14.

The CI matrix defines the supported Python versions. A newer Python version is considered supported after it has been added to the matrix and passes the complete workflow.

## Limitations

- Brightness, contrast, and blur score are descriptive statistics, not absolute image-quality measurements.
- Useful thresholds depend on image content, resolution, acquisition conditions, bit depth, and the downstream task.
- The Laplacian variance is sensitive to texture and noise as well as blur. A highly textured image can receive a high score even when the score is not useful for a particular application.
- Metric values are not normalized across different image bit depths.
- Only JPEG and PNG filename extensions are inspected in version 0.1.x.
- EXIF orientation is not normalized or reported.
- Annotation files, duplicate images, and dataset labels are outside the current scope.
- The implementation is designed for small and moderate local datasets, not large-scale or distributed processing.

## Reproducibility

Regenerate the synthetic fixture and its report:

```bash
python examples/generate_demo_images.py --output output/demo_images
image-dataset-inspector inspect output/demo_images \
  --output output/report.csv
```

Regenerate the checksum-verified public sample, CSV, and contact sheet:

```bash
python examples/run_public_sample.py \
  --images output/public-sample/images \
  --output output/public-sample
```

Candidate paths are sorted before inspection, relative paths use POSIX form,
and metric values are written with six decimal places. The public-sample
script fixes the downloaded bytes with SHA-256 checks before generating its
artifacts.

## Compatibility

Python 3.10 through 3.14 are tested in CI. Version 0.1.x supports recursive
`.jpg`, `.jpeg`, and `.png` discovery, the documented `inspect` command and
exit codes, and the current CSV columns. The project does not claim a 1.x
stability guarantee; consumers that require a fixed interface should pin a
release and review changes before upgrading.

## Project Structure

```text
image-dataset-inspector/
├── .github/
│   └── workflows/
│       └── ci.yml
├── examples/
│   ├── public_sample/
│   │   ├── README.md
│   │   ├── public_sample_contact_sheet.jpg
│   │   └── public_sample_report.csv
│   ├── generate_demo_images.py
│   └── run_public_sample.py
├── src/
│   └── image_dataset_inspector/
│       ├── __init__.py
│       ├── cli.py
│       ├── inspector.py
│       ├── metrics.py
│       └── reporting.py
├── tests/
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_inspector.py
│   └── test_metrics.py
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

## Roadmap

Possible later improvements include optional JSON output, configurable checks, duplicate detection, and richer summary reports. They are intentionally excluded from version 0.1.x to keep the initial implementation small and auditable.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
