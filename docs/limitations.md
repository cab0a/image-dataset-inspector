# Limitations

## 日本語概要

本書は、明るさ、コントラスト、ラプラシアン分散が画像品質の絶対値ではないことを明確にします。対応形式、ビット深度、EXIFの向き、重複・ラベル検査、処理規模、および終了コードから判断できる範囲の制約を記録しています。

現在の適用範囲と将来候補は以下の英語本文を参照してください。

---

## English Summary

This document bounds what the reported image statistics and CLI success state
can establish. It also records unsupported formats, metadata behavior,
dataset-scale limits, and inputs that remain outside version `0.1.x`.

## Documented Constraints

- Brightness, contrast, and blur score are descriptive statistics, not absolute image-quality measurements.
- Acceptance thresholds depend on image content, resolution, acquisition conditions, bit depth, and the downstream task.
- Laplacian variance is sensitive to texture and noise as well as blur. A highly textured image can receive a high score even when it is unsuitable for a particular application.
- Metric values are not normalized across different image bit depths.
- Version `0.1.x` inspects only `.jpg`, `.jpeg`, and `.png` filename extensions.
- EXIF orientation is not normalized or reported.
- Annotation files, duplicate images, and dataset labels are outside the current scope.
- The implementation targets small and moderate local datasets, not large-scale or distributed processing.
- Public-sample images do not provide semantic image-quality labels.
- A successful exit code confirms report generation, not that every candidate image is valid.

Possible later additions include optional JSON output, configurable checks, duplicate detection, and richer summary reports. They are excluded from version `0.1.x` to keep the current behavior narrow and auditable.
