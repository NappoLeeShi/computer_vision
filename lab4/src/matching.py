"""Compare image pairs using Wavelet Hashes and Hamming distance."""

import sys
from collections.abc import Sequence
from pathlib import Path

if __package__:
    from .wavelet_hash import generate_wavelet_hash, hamming_distance
else:
    from wavelet_hash import generate_wavelet_hash, hamming_distance


DEFAULT_THRESHOLD = 20


def compare_images(
    image1_path: str | Path,
    image2_path: str | Path,
    threshold: int = DEFAULT_THRESHOLD,
) -> dict[str, object]:
    """Compare two image files and return their predicted similarity result."""
    if threshold < 0:
        raise ValueError("The threshold must be non-negative.")

    first_hash = generate_wavelet_hash(image1_path)
    second_hash = generate_wavelet_hash(image2_path)
    distance = hamming_distance(first_hash, second_hash)
    predicted_label = int(distance <= threshold)

    return {
        "image1_path": str(image1_path),
        "image2_path": str(image2_path),
        "hamming_distance": distance,
        "threshold": threshold,
        "predicted_label": predicted_label,
    }


def compare_image_pairs(
    pairs: Sequence[tuple[str | Path, str | Path, int]],
    threshold: int = DEFAULT_THRESHOLD,
) -> list[dict[str, object]]:
    """Compare labeled image pairs given as path, path, label tuples."""
    if threshold < 0:
        raise ValueError("The threshold must be non-negative.")

    results = []
    for image1_path, image2_path, ground_truth in pairs:
        if ground_truth not in (0, 1):
            raise ValueError("Ground-truth labels must be 0 or 1.")

        result = compare_images(image1_path, image2_path, threshold)
        result["ground_truth"] = ground_truth
        results.append(result)

    return results


if __name__ == "__main__":
    print("Usage: python src/matching.py <image1_path> <image2_path> [threshold]")
    if len(sys.argv) < 3:
        print("No image paths were provided; comparison demo skipped.")
    else:
        try:
            demo_threshold = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_THRESHOLD
            print(compare_images(sys.argv[1], sys.argv[2], demo_threshold))
        except (OSError, ValueError) as error:
            print(f"Could not compare the images: {error}")
