"""Generate balanced similar and dissimilar image-pair datasets."""

import argparse
import itertools
import random
import shutil
from collections.abc import Sequence
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "original_images"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data"
DEFAULT_OUTPUT_FORMAT = "jpg"
DEFAULT_SEED = 42
DEFAULT_UNCHANGED_PROBABILITY = 0.2
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
TRANSFORMATIONS = ("rotation", "brightness", "noise", "flip", "resize")


def find_source_images(source_dir: str | Path) -> list[Path]:
    """Return supported image files in a deterministic order."""
    source_dir = Path(source_dir)
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    return sorted(
        (
            path
            for path in source_dir.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ),
        key=lambda path: path.name.lower(),
    )


def load_rgb_image(image_path: str | Path) -> Image.Image:
    """Load an image and return an independent RGB copy."""
    with Image.open(Path(image_path)) as image:
        return image.convert("RGB")


def transform_image(
    image: Image.Image,
    transformation: str,
    rng: random.Random,
) -> Image.Image:
    """Apply exactly one small transformation to an image."""
    if transformation == "rotation":
        angle = rng.uniform(-8.0, 8.0)
        return image.rotate(angle, resample=Image.Resampling.BICUBIC)

    if transformation == "brightness":
        factor = rng.uniform(0.9, 1.1)
        return ImageEnhance.Brightness(image).enhance(factor)

    if transformation == "noise":
        width, height = image.size
        noise_bytes = rng.randbytes(width * height)
        noise = Image.frombytes("L", image.size, noise_bytes).convert("RGB")
        return Image.blend(image, noise, alpha=0.08)

    if transformation == "flip":
        return ImageOps.mirror(image)

    if transformation == "resize":
        width, height = image.size
        scale = rng.uniform(0.95, 1.05)
        new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
        return image.resize(new_size, resample=Image.Resampling.BICUBIC)

    raise ValueError(f"Unknown transformation: {transformation}")


def split_pair_counts(total_pairs: int) -> tuple[int, int]:
    """Split total pairs as evenly as possible into similar and dissimilar."""
    if total_pairs < 1:
        raise ValueError("The number of pairs must be at least 1.")
    similar_pairs = total_pairs // 2
    return similar_pairs, total_pairs - similar_pairs


def save_image(
    image: Image.Image,
    image_path: str | Path,
    output_format: str,
) -> None:
    """Save one image in the selected output format."""
    image_path = Path(image_path)
    if output_format == "jpg":
        image.save(image_path, format="JPEG", quality=95)
    elif output_format == "png":
        image.save(image_path, format="PNG")
    else:
        raise ValueError("Output format must be 'jpg' or 'png'.")


def save_pair(
    pair_dir: Path,
    image1: Image.Image,
    image2: Image.Image,
    output_format: str,
) -> None:
    """Save two images using predictable names inside a pair directory."""
    pair_dir.mkdir(parents=True, exist_ok=False)
    extension = ".jpg" if output_format == "jpg" else ".png"
    save_image(image1, pair_dir / f"image1{extension}", output_format)
    save_image(image2, pair_dir / f"image2{extension}", output_format)


def prepare_output_directories(output_dir: str | Path, clear: bool) -> None:
    """Create output categories and optionally clear old generated pairs."""
    output_dir = Path(output_dir)
    category_dirs = (output_dir / "similar", output_dir / "dissimilar")
    if clear:
        for category_dir in category_dirs:
            if category_dir.exists() and not category_dir.is_dir():
                raise ValueError(f"Cannot clear non-directory path: {category_dir}")
            if category_dir.exists():
                shutil.rmtree(category_dir)

    for category_dir in category_dirs:
        category_dir.mkdir(parents=True, exist_ok=True)
        if not clear and any(category_dir.iterdir()):
            raise ValueError(
                f"Generated pairs already exist in {category_dir}; use clear=True."
            )


def generate_similar_pairs(
    source_images: Sequence[Path],
    output_dir: Path,
    pair_count: int,
    rng: random.Random,
    unchanged_probability: float,
    output_format: str,
) -> None:
    """Generate similar pairs from the same source image."""
    for pair_number in range(1, pair_count + 1):
        source_path = rng.choice(source_images)
        image1 = load_rgb_image(source_path)
        if rng.random() < unchanged_probability:
            image2 = image1.copy()
        else:
            transformation = rng.choice(TRANSFORMATIONS)
            image2 = transform_image(image1, transformation, rng)

        save_pair(
            output_dir / "similar" / f"pair_{pair_number:02d}",
            image1,
            image2,
            output_format,
        )


def generate_dissimilar_pairs(
    source_images: Sequence[Path],
    output_dir: Path,
    pair_count: int,
    rng: random.Random,
    output_format: str,
) -> None:
    """Generate dissimilar pairs from different source images."""
    source_pairs = list(itertools.combinations(source_images, 2))
    rng.shuffle(source_pairs)
    for pair_number, (source1, source2) in enumerate(
        source_pairs[:pair_count], start=1
    ):
        save_pair(
            output_dir / "dissimilar" / f"pair_{pair_number:02d}",
            load_rgb_image(source1),
            load_rgb_image(source2),
            output_format,
        )


def generate_dataset(
    source_dir: str | Path = DEFAULT_SOURCE_DIR,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    pair_count: int | None = None,
    unchanged_probability: float = DEFAULT_UNCHANGED_PROBABILITY,
    seed: int = DEFAULT_SEED,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    clear: bool = False,
) -> dict[str, int | float]:
    """Generate a reproducible, approximately balanced image-pair dataset."""
    if not 0.0 <= unchanged_probability <= 1.0:
        raise ValueError("unchanged_probability must be between 0 and 1.")
    if output_format not in {"jpg", "png"}:
        raise ValueError("output_format must be 'jpg' or 'png'.")

    source_dir = Path(source_dir).resolve()
    output_dir = Path(output_dir).resolve()
    if source_dir == output_dir or source_dir in output_dir.parents:
        raise ValueError("The output directory cannot be inside original_images.")

    source_images = find_source_images(source_dir)
    if len(source_images) < 2:
        raise ValueError("At least two supported source images are required.")

    if pair_count is None:
        pair_count = len(source_images)
    if pair_count < 1:
        raise ValueError("The number of pairs must be at least 1.")

    similar_count, dissimilar_count = split_pair_counts(pair_count)
    maximum_dissimilar_pairs = len(source_images) * (len(source_images) - 1) // 2
    if dissimilar_count > maximum_dissimilar_pairs:
        raise ValueError(
            "The requested dissimilar-pair count exceeds the number of unique pairs."
        )

    prepare_output_directories(output_dir, clear)
    rng = random.Random(seed)
    generate_similar_pairs(
        source_images,
        output_dir,
        similar_count,
        rng,
        unchanged_probability,
        output_format,
    )
    generate_dissimilar_pairs(
        source_images,
        output_dir,
        dissimilar_count,
        rng,
        output_format,
    )

    return {
        "source_images": len(source_images),
        "total_pairs": similar_count + dissimilar_count,
        "similar_pairs": similar_count,
        "dissimilar_pairs": dissimilar_count,
        "similar_ratio": similar_count / (similar_count + dissimilar_count),
        "dissimilar_ratio": dissimilar_count / (similar_count + dissimilar_count),
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for dataset generation."""
    parser = argparse.ArgumentParser(
        description="Generate similar and dissimilar image-pair datasets."
    )
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--pairs",
        "--pair-count",
        type=int,
        default=None,
        help="Total number of pairs; defaults to the source-image count.",
    )
    parser.add_argument(
        "--unchanged-probability",
        "--unchanged_probability",
        type=float,
        default=DEFAULT_UNCHANGED_PROBABILITY,
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=("jpg", "png"),
        default=DEFAULT_OUTPUT_FORMAT,
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Remove existing generated pairs before writing new ones.",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    """Run dataset generation from the command line."""
    parser = build_parser()
    options = parser.parse_args(arguments)
    try:
        summary = generate_dataset(
            source_dir=options.source_dir,
            output_dir=options.output_dir,
            pair_count=options.pairs,
            unchanged_probability=options.unchanged_probability,
            seed=options.seed,
            output_format=options.output_format,
            clear=options.clear,
        )
    except (OSError, ValueError) as error:
        print(f"Dataset generation failed: {error}")
        return 1

    total_pairs = int(summary["total_pairs"])
    print(f"Source images detected: {summary['source_images']}")
    print(f"Generated pairs: {total_pairs}")
    print(
        f"Similar pairs: {summary['similar_pairs']} "
        f"({float(summary['similar_ratio']):.1%})"
    )
    print(
        f"Dissimilar pairs: {summary['dissimilar_pairs']} "
        f"({float(summary['dissimilar_ratio']):.1%})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
