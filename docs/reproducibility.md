# Reproducibility

## 日本語概要

本書は、5枚の正常画像と1件の不正JPEGからなる合成標本、およびSHA-256で固定した公開画像標本を再生成・検査する手順をまとめています。探索順、相対パス、数値書式、端末表示を固定し、対応Python版の自動テスト内容も記録しています。

環境構築と検証コマンドは以下の英語本文を参照してください。

---

## English Summary

This guide defines the synthetic and public-image workflows used to verify
file discovery, per-image metrics, unreadable-file handling, deterministic
ordering, CSV formatting, and supported Python versions.

## Environment

Python 3.10 through 3.14 are tested in GitHub Actions. The runtime dependencies are NumPy and `opencv-python-headless`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Synthetic Fixture

Generate five decodable images and one deliberately invalid JPEG, then inspect them:

```bash
python examples/generate_demo_images.py --output output/demo_images
image-dataset-inspector inspect output/demo_images \
  --output output/report.csv
```

Expected summary:

```text
Scanned: 6
Valid: 5
Unreadable: 1
Report: output/report.csv
```

The fixture includes dark and bright images, a checkerboard and blurred counterpart, a color gradient, and a corrupt JPEG. It supports relative metric checks and the decode-failure path without private data.

## Public Sample

Generate a CSV report and contact sheet from five freely reusable scikit-image samples:

```bash
python examples/run_public_sample.py \
  --images output/public-sample/images \
  --output output/public-sample
```

The first run requires network access. Source URLs are pinned to scikit-image `v0.26.0`, and each downloaded byte sequence is verified with SHA-256 before inspection.

The committed reference outputs are:

- [`examples/public_sample/public_sample_report.csv`](../examples/public_sample/public_sample_report.csv)
- [`examples/public_sample/public_sample_contact_sheet.jpg`](../examples/public_sample/public_sample_contact_sheet.jpg)

The [public sample report](../examples/public_sample/README.md) documents interpretation, provenance, and licenses.

## Deterministic Controls

- Synthetic arrays and the corrupt JPEG contents are generated directly in code.
- Candidate paths are sorted before inspection.
- Relative paths use POSIX separators.
- CSV column order is fixed.
- Numeric metrics use six decimal places.
- Public source bytes are checked against committed SHA-256 values.

The project does not claim byte-identical JPEG contact-sheet encoding across every OpenCV build.

## Verification in CI

GitHub Actions installs the package, verifies the CLI entry point, and runs eight tests on Python 3.10 through 3.14.

The tests cover:

- recursive valid-image discovery;
- corrupt-image reporting;
- CSV generation and column order;
- relative brightness, contrast, and blur-score behavior;
- invalid-input exit code `2`;
- unwritable-output exit code `1`.

These tests use relative metric behavior instead of fixed metric values that could be brittle across image-processing library versions.
