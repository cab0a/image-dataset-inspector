# Public Image Sample

This example applies Image Dataset Inspector to five real images distributed with scikit-image. The download URLs are pinned to scikit-image `v0.26.0`, and every file is verified with SHA-256 before use.

The source images are downloaded at runtime and are not committed to this repository. The generated CSV report and contact sheet are committed so the result can be reviewed without downloading the originals.

## Reproduction

From an installed development environment:

```bash
python examples/run_public_sample.py
```

Expected summary:

```text
Images: 5
Valid: 5
Report: examples/public_sample/public_sample_report.csv
Contact sheet: examples/public_sample/public_sample_contact_sheet.jpg
```

## Interpretation

The report is intended to demonstrate how the metrics behave on varied photographs, not to rank image quality.

| Image | Brightness | Contrast | Blur score |
| --- | ---: | ---: | ---: |
| `camera.png` | 129.1 | 73.6 | 1133.2 |
| `clock_motion.png` | 146.3 | 20.9 | 24.3 |
| `coffee.png` | 103.7 | 58.1 | 1541.2 |
| `hubble_deep_field.jpg` | 19.4 | 26.2 | 537.2 |
| `rocket.jpg` | 61.0 | 30.6 | 820.9 |

The motion-blurred clock has the lowest contrast and Laplacian variance despite having the highest mean brightness. This is consistent with its deliberately blurred content. The coffee image produces the highest blur score because it contains strong edges, texture, and small highlights; the value should not be interpreted as a universal measure of photographic quality.

The Hubble image has by far the lowest mean brightness but retains a substantial blur score because small bright objects create local intensity changes. The camera and rocket images also show that edge density, scene content, and resolution affect Laplacian variance. These results support using the metrics for within-dataset investigation and outlier review rather than applying one threshold across unrelated image categories.

## Sources and Licenses

| File | Source and attribution | License |
| --- | --- | --- |
| `camera.png` | Photograph by Lav Varshney, distributed in [`skimage.data.camera`](https://scikit-image.org/docs/stable/api/skimage.data#skimage.data.camera) | CC0 |
| `coffee.png` | Photograph by Rachel Michetti, distributed in [`skimage.data.coffee`](https://scikit-image.org/docs/stable/api/skimage.data#skimage.data.coffee) | CC0 |
| `clock_motion.png` | Photograph by Stefan van der Walt, distributed in [`skimage.data.clock`](https://scikit-image.org/docs/stable/api/skimage.data#skimage.data.clock) | Public domain |
| `rocket.jpg` | SpaceX launch photograph, distributed in [`skimage.data.rocket`](https://scikit-image.org/docs/stable/api/skimage.data#skimage.data.rocket) | Public domain |
| `hubble_deep_field.jpg` | NASA Hubble Deep Field image, distributed in [`skimage.data.hubble_deep_field`](https://scikit-image.org/docs/stable/api/skimage.data#skimage.data.hubble_deep_field) | Public domain |

See the [scikit-image data documentation](https://scikit-image.org/docs/stable/api/skimage.data) for the upstream descriptions and licensing notes.
