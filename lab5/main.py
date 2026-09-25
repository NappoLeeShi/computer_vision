"""Real-time face recognition from the physical webcam.

This is the integration layer of Practical Assignment 5. It joins the four
modules that were built separately and runs them as one continuous real-time
loop:

    data/faces/  ->  MTCNN + FaceNet  ->  reference embeddings   (once, at start)
    webcam       ->  MTCNN            ->  face crops             (every frame)
                 ->  FaceNet          ->  live embeddings        (every frame)
                 ->  cosine similarity->  threshold 0.7          (every frame)
                 ->  draw + display   ->  the labelled frame     (every frame)

The webcam is the live input. The photos in ``data/faces/`` are only the
registered examples used to build the reference embeddings; they are read once
before the loop starts and are never treated as live input.

Division of work
----------------
Every responsibility stays in the module that owns it, and this file only wires
them together:

    face_detector.detect_faces(frame)               -> faces, boxes, crops
    face_embedding.generate_embedding(face_crop)    -> 512-d embedding
    face_matching.match_embedding(live, refs, 0.7)  -> label + similarity
    webcam.run_webcam_loop(on_frame=...)            -> the live loop

No model is created here. MTCNN and FaceNet are loaded once inside their own
modules and reused, so the loop only pays for inference.

Usage
-----
    python main.py
    python main.py --camera 0 --threshold 0.7 --data-dir data/faces

Press q in the video window to exit.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

from src.face_detector import detect_faces
from src.face_embedding import generate_embedding
from src.face_matching import UNKNOWN_LABEL, match_embedding
from src.webcam import run_webcam_loop


PROJECT_ROOT = Path(__file__).resolve().parent

DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "faces"
DEFAULT_CAMERA_INDEX = 0
DEFAULT_THRESHOLD = 0.7

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff")

# Simple OpenCV drawing settings for the face boxes and their labels.
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 1
BOX_THICKNESS = 2
MATCHED_COLOR = (0, 255, 0)
UNKNOWN_COLOR = (0, 0, 255)


def load_reference_embeddings(data_dir: Path) -> dict[str, list[np.ndarray]]:
    """Build the reference embeddings from the photos in ``data_dir``.

    Each subdirectory of ``data_dir`` is one known identity, named after the
    folder. Every image in it contributes one embedding, so a person with three
    photos ends up with three reference embeddings to be compared against.

    The photo is passed through the same MTCNN detector as a webcam frame
    before FaceNet sees it, and the most confidently detected face is embedded.
    That matters: FaceNet expects a tight face crop, and feeding it a whole
    photo with background produces an embedding that no longer matches the same
    person seen on the webcam, so recognition would fail. Using the existing
    detector here keeps the reference path and the live path identical.

    Arguments:
        data_dir {Path} -- folder holding one subdirectory per identity.

    Returns:
        dict -- ``{"person_01": [embedding, ...], "person_02": [...]}``, the
        structure expected by ``face_matching.match_embedding()``.

    Raises:
        FileNotFoundError -- if the folder does not exist.
        RuntimeError -- if it holds no usable reference image, which would leave
            the application with nobody to recognise.
    """
    if not data_dir.is_dir():
        raise FileNotFoundError(
            f"The reference image folder does not exist: {data_dir}\n"
            "Create it and put one subfolder of reference photos per person "
            "inside it, for example data/faces/person_01/image01.jpg."
        )

    references: dict[str, list[np.ndarray]] = {}

    for identity_dir in sorted(path for path in data_dir.iterdir() if path.is_dir()):
        embeddings: list[np.ndarray] = []

        for image_path in sorted(identity_dir.iterdir()):
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            # face_embedding.generate_embedding expects BGR uint8 images,
            # which is exactly what cv2.imread returns.
            image = cv2.imread(str(image_path))
            if image is None:
                print(f"  Warning: could not read {image_path}, skipping it.")
                continue

            faces = detect_faces(image)
            if not faces:
                print(f"  Warning: no face found in {image_path}, skipping it.")
                continue

            # A reference photo may contain bystanders, so only the most
            # confident face is registered as this identity.
            best_face = max(faces, key=lambda face: face["confidence"])
            embeddings.append(generate_embedding(best_face["face"]))

        if not embeddings:
            # An identity with no usable photo is left out instead of being
            # registered as an empty entry.
            print(f"  Warning: no usable reference photo for {identity_dir.name}, skipping it.")
            continue

        references[identity_dir.name] = embeddings
        print(f"  {identity_dir.name}: {len(embeddings)} reference embedding(s)")

    if not references:
        raise RuntimeError(
            f"No usable reference image was found in {data_dir}.\n"
            "Add at least one clear photo per person, one subfolder per person, "
            "for example data/faces/person_01/image01.jpg."
        )

    return references


def draw_result(
    frame: np.ndarray, box: tuple[int, int, int, int], result: dict[str, object]
) -> None:
    """Draw one face box with its identity and similarity on the frame.

    A matched face is drawn in green and an unknown one in red, so the outcome
    is readable at a glance. The label is placed above the box, or below it when
    there is no room above.
    """
    x1, y1, x2, y2 = box
    label = str(result["label"])
    matched = label != UNKNOWN_LABEL
    color = MATCHED_COLOR if matched else UNKNOWN_COLOR

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, BOX_THICKNESS)

    text = f"{label} {float(result['similarity']):.2f}"
    (text_width, text_height), _ = cv2.getTextSize(
        text, FONT, FONT_SCALE, FONT_THICKNESS
    )

    above = y1 - text_height - 6
    if above > text_height:
        position = (x1, above)
    else:
        position = (x1, min(y2 + text_height + 6, frame.shape[0] - 4))

    cv2.putText(
        frame, text, position, FONT, FONT_SCALE, color, FONT_THICKNESS, cv2.LINE_AA
    )


def process_frame(
    frame: np.ndarray,
    reference_embeddings: dict[str, list[np.ndarray]],
    threshold: float,
) -> np.ndarray:
    """Run the recognition pipeline on one live webcam frame.

    Every face in the frame is detected, embedded and matched independently, so
    several people in the shot are all recognised at once. A frame with no face
    is a normal real-time condition: it is returned untouched, with no label
    drawn, and the loop carries on.

    Arguments:
        frame {np.ndarray} -- the live BGR frame from the webcam.
        reference_embeddings {dict} -- the identities built once at start-up.
        threshold {float} -- the similarity threshold, 0.7 by default.

    Returns:
        np.ndarray -- the same frame with the results drawn on it, which is what
        the webcam window displays.
    """
    faces = detect_faces(frame)

    # All embeddings are computed before anything is drawn. The face crops are
    # slices of the frame itself, so drawing a box first could alter the pixels
    # that a later face is embedded from.
    results = []
    for face in faces:
        embedding = generate_embedding(face["face"])
        result = match_embedding(embedding, reference_embeddings, threshold)
        results.append((face["box"], result))

    for box, result in results:
        draw_result(frame, box, result)

    return frame


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the few command-line options the application supports."""
    parser = argparse.ArgumentParser(
        description="Real-time face recognition with FaceNet and MTCNN on the webcam."
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=DEFAULT_CAMERA_INDEX,
        help="index of the webcam to open (default: %(default)s)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="similarity threshold for a match (default: %(default)s)",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="folder holding one subfolder of reference photos per person "
        "(default: %(default)s)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Start the application: build the references, then run the live loop."""
    args = parse_args(argv)

    # Checked once here so a bad value is reported before the camera is opened,
    # instead of failing on the first frame inside the loop.
    if not -1.0 <= args.threshold <= 1.0:
        print(
            f"Error: the threshold must be between -1.0 and 1.0, got {args.threshold}."
        )
        return 1
    if args.camera < 0:
        print(f"Error: the camera index must be zero or positive, got {args.camera}.")
        return 1

    try:
        print("Loading reference embeddings...")
        reference_embeddings = load_reference_embeddings(args.data_dir)
        print(
            f"Loaded identities: {', '.join(reference_embeddings)} "
            f"(threshold {args.threshold})"
        )

        print("Starting webcam...")
        run_webcam_loop(
            camera_index=args.camera,
            on_frame=lambda frame: process_frame(frame, reference_embeddings, args.threshold),
        )
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"Error: {error}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
