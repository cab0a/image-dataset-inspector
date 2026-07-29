# Report Schema and Metrics

The `inspect` command writes one UTF-8 CSV row for each discovered image candidate.

## Columns

Column order is fixed by `CSV_COLUMNS` in `reporting.py`.

| Column | Description |
| --- | --- |
| `relative_path` | POSIX-style path relative to the inspected directory |
| `file_size_bytes` | File size in bytes |
| `width` | Decoded image width in pixels |
| `height` | Decoded image height in pixels |
| `channels` | Number of decoded image channels |
| `brightness` | Arithmetic mean of grayscale intensity |
| `contrast` | Standard deviation of grayscale intensity |
| `blur_score` | Variance of the grayscale Laplacian |
| `status` | `valid` or `unreadable` |
| `error_message` | Explanation when inspection fails; otherwise empty |

Unavailable values are empty fields. Metric values use six decimal places. The writer uses `\n` line endings.

## Example

```csv
relative_path,file_size_bytes,width,height,channels,brightness,contrast,blur_score,status,error_message
bright.png,432,128,128,3,224.000000,0.000000,0.000000,valid,
broken.jpg,31,,,,,,,unreadable,OpenCV could not decode the image.
```

## Decode and Channel Handling

OpenCV loads each file with `cv2.IMREAD_UNCHANGED`.

- A two-dimensional image is treated as one channel.
- A three-channel image is converted from BGR to grayscale.
- A four-channel image is converted from BGRA to grayscale.
- A decoded image with another channel count is recorded as unreadable when metric calculation fails.

The report preserves the original decoded channel count while calculating all three metrics from the grayscale representation.

## Metric Definitions

### Brightness

`brightness` is the arithmetic mean of the grayscale array.

A larger value means a larger mean grayscale intensity for that decoded image. Values are not normalized across different bit depths.

### Contrast

`contrast` is the population standard deviation of grayscale intensities, as returned by `numpy.std`.

It describes intensity spread within one image. It does not measure semantic visibility or suitability for a downstream task.

### Blur score

`blur_score` is the variance of `cv2.Laplacian(grayscale, cv2.CV_64F)`.

Higher-frequency edges and texture can increase the score. Blur can lower it, but image content, noise, resolution, and scale also affect the value. It is not an absolute sharpness or image-quality score.

## Ordering and Repeatability

Candidate paths are sorted before inspection, so unchanged directory contents produce a stable row order on the same supported environment. Relative paths are serialized with `/`, and numeric metrics are formatted to six decimal places.

See [Limitations](limitations.md) before defining acceptance thresholds from these descriptive values.
