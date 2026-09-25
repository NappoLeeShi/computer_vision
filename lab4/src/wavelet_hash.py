"""Wavelet-based image preprocessing, hashing, and Hamming distance utilities."""

import sys
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pywt
from PIL import Image


DEFAULT_IMAGE_SIZE = (32, 32)
DEFAULT_WAVELET = "haar"


def load_and_preprocess_image(
    image_path: str | Path,
    image_size: tuple[int, int] = DEFAULT_IMAGE_SIZE,
) -> np.ndarray:
    """Load an image, convert it to grayscale, and resize it consistently."""
    width, height = image_size
    if width < 2 or height < 2:
        raise ValueError("Image dimensions must both be at least 2 pixels.")

    with Image.open(image_path) as image:
        grayscale_image = image.convert("L")
        resized_image = grayscale_image.resize(
            (width, height), Image.Resampling.LANCZOS
        )
        return np.asarray(resized_image, dtype=np.float64)


def wavelet_transform(
    image: np.ndarray,
    wavelet: str = DEFAULT_WAVELET,
) -> tuple[np.ndarray, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Return the one-level approximation and detail wavelet coefficients."""
    image_array = np.asarray(image, dtype=np.float64)
    if image_array.ndim != 2 or min(image_array.shape) < 2:
        raise ValueError("The input image must be a 2D array at least 2x2 pixels.")

    approximation, details = pywt.dwt2(image_array, wavelet)
    return approximation, details


def quantize_coefficients(
    coefficients: np.ndarray,
    threshold: float | None = None,
) -> np.ndarray:
    """Convert selected approximation coefficients to binary values using their mean."""
    coefficient_array = np.asarray(coefficients, dtype=np.float64)
    if coefficient_array.size == 0:
        raise ValueError("Coefficient selection cannot be empty.")

    if threshold is None:
        threshold = float(np.mean(coefficient_array))
    return (coefficient_array > threshold).astype(np.uint8).reshape(-1)


def generate_wavelet_hash(
    image_path: str | Path,
    image_size: tuple[int, int] = DEFAULT_IMAGE_SIZE,
    wavelet: str = DEFAULT_WAVELET,
    threshold: float | None = None,
) -> np.ndarray:
    """Generate a binary wavelet hash from an image file."""
    preprocessed_image = load_and_preprocess_image(image_path, image_size)
    approximation_coefficients, _ = wavelet_transform(preprocessed_image, wavelet)
    return quantize_coefficients(approximation_coefficients, threshold)


def hamming_distance(
    first_hash: Sequence[int] | np.ndarray,
    second_hash: Sequence[int] | np.ndarray,
) -> int:
    """Return the number of differing bits between two binary hashes."""
    first_array = np.asarray(first_hash)
    second_array = np.asarray(second_hash)
    if first_array.shape != second_array.shape:
        raise ValueError("Hashes must have the same shape.")
    return int(np.count_nonzero(first_array != second_array))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("A real image path is required; no test image is assumed.")
        print("Usage: python src/wavelet_hash.py <image_path>")
    else:
        try:
            example_hash = generate_wavelet_hash(sys.argv[1])
            print(f"Wavelet hash ({example_hash.size} bits): {example_hash}")
        except (OSError, ValueError) as error:
            print(f"Could not generate the wavelet hash: {error}")
