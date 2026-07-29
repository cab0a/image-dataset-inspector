# Limitations

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
