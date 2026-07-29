# Command-Line Interface

## 日本語概要

本書は、画像フォルダーを再帰検査する`inspect`コマンドの引数、対象拡張子、探索順序、端末表示、終了コード、ファイル単位の失敗処理を定義します。Pythonから利用できる範囲と、0.1.xで維持する互換性の境界も記載しています。

完全な操作仕様は以下の英語本文を参照してください。

---

## English Summary

This document defines the command-line behavior of Image Dataset Inspector version `0.1.x`.

## Command

```text
image-dataset-inspector inspect INPUT_DIRECTORY --output REPORT.csv
```

| Argument | Meaning |
| --- | --- |
| `inspect` | Recursively inspect supported image files |
| `INPUT_DIRECTORY` | Readable directory used as the scan root |
| `--output REPORT.csv` | Required destination for the UTF-8 CSV report |

The output directory is created when necessary. The report path itself must be writable.

## File Discovery

The scanner:

1. walks the input directory recursively;
2. keeps regular files with case-insensitive `.jpg`, `.jpeg`, or `.png` suffixes;
3. sorts candidate paths before inspection;
4. writes paths relative to the scan root using POSIX separators.

Files with other extensions are ignored, even when their bytes contain a supported image format.

## Terminal Summary

A completed scan prints:

```text
Scanned: 6
Valid: 5
Unreadable: 1
Report: output/report.csv
```

`Scanned` counts supported filename candidates. `Unreadable` includes metadata, decode, and metric-calculation failures recorded in the CSV.

## Exit Codes

| Exit code | Meaning |
| ---: | --- |
| `0` | The scan completed and the CSV report was written |
| `1` | The CSV report could not be written |
| `2` | The input path was not a readable directory |

Unreadable image rows do not change a successful scan to a non-zero exit code. Argument parsing errors follow the default `argparse` behavior and also exit with code `2`.

## Per-File Failure Behavior

The scanner does not propagate expected read failures from one file to the whole dataset.

| Failure stage | CSV status | Error message |
| --- | --- | --- |
| File metadata | `unreadable` | `Could not read file metadata.` |
| OpenCV decode | `unreadable` | `OpenCV could not decode the image.` |
| Metric calculation | `unreadable` | `The image was decoded, but its metrics could not be calculated.` |

Unavailable dimensions or metrics are written as empty CSV fields. Other candidates continue through the pipeline.

## Python Import Surface

The package root exposes `image_dataset_inspector.__version__`. The modules under `image_dataset_inspector` are used by the CLI and examples, but version `0.1.x` does not declare a stable Python API contract for them.

## Compatibility Boundary

Version `0.1.x` documents:

- the `inspect` command and its arguments;
- exit codes `0`, `1`, and `2`;
- recursive `.jpg`, `.jpeg`, and `.png` discovery;
- the CSV columns and status values in the [report schema](report-schema.md).

The project does not claim a `1.x` stability guarantee. Pin a release and review changes before upgrading when a fixed interface is required.
