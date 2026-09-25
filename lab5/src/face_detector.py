"""Face detection with MTCNN.

MTCNN (Multi-task Cascaded Convolutional Networks) is the face detector used in
this practical assignment. It is a cascade of three small convolutional
networks (P-Net, R-Net, O-Net) that are applied in stages on an image pyramid:

    1. P-Net proposes many candidate regions on a scaled pyramid of the image.
    2. R-Net rejects the weak candidates.
    3. O-Net confirms the remaining ones and refines their coordinates.

Because the detector is fully convolutional it is applied to a single frame very
quickly, which is what makes the real-time webcam loop possible. The three nets
are used exactly as they were pre-trained; nothing is trained here.

Input / output of the public interface
--------------------------------------
``detect_faces(frame)`` takes one image and returns a list of detected faces.
Every item of that list is a plain ``dict`` with three keys:

    "box"        (x1, y1, x2, y2) -- the bounding box of the face, in pixels of
                 the input frame, as the top-left and bottom-right corners.
    "confidence" float in [0, 1] -- how sure the detector is that the box
                 really contains a face (the output score of O-Net).
    "face"       the face crop itself, as a NumPy array in the same BGR colour
                 order and at the original scale as the input frame.

A frame containing no face is not an error: the function simply returns an
empty list, and the caller decides what to display.

How the next stage uses this
----------------------------
The FaceNet stage takes each ``"face"`` crop and turns it into an embedding
vector. The crop is returned at its original scale and in OpenCV BGR order on
purpose: resizing and colour conversion for FaceNet belong to the embedding
module, so this module stays focused on detection only.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from facenet_pytorch import MTCNN


DEFAULT_MIN_FACE_SIZE = 20
DEFAULT_THRESHOLDS = (0.6, 0.7, 0.7)

_detector: MTCNN | None = None


def _get_detector() -> MTCNN:
    """Return the shared MTCNN detector, creating it on first use.

    Building the detector loads the pre-trained P-Net, R-Net and O-Net weights.
    It is done once and reused, because rebuilding it for every frame would be
    far too slow for a real-time loop.
    """
    global _detector
    if _detector is None:
        _detector = MTCNN(
            min_face_size=DEFAULT_MIN_FACE_SIZE,
            thresholds=list(DEFAULT_THRESHOLDS),
        )
    return _detector


def read_image(image_path: str | Path) -> np.ndarray:
    """Read an image file into a BGR NumPy array, the format OpenCV uses.

    This is the same format the webcam produces, so an image read from disk and
    a live webcam frame can be given to ``detect_faces`` in the same way.
    """
    frame = cv2.imread(str(image_path))
    if frame is None:
        raise ValueError(f"Could not read the image: {image_path}")
    return frame


def _check_frame(frame: np.ndarray) -> np.ndarray:
    """Validate a frame and return it as a contiguous BGR array.

    OpenCV always hands out uint8 BGR arrays, so anything else means the caller
    passed something that is not a usable camera frame.
    """
    if not isinstance(frame, np.ndarray):
        raise ValueError("The frame must be a NumPy array as returned by OpenCV.")
    if frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError(
            f"The frame must have shape (height, width, 3), got {frame.shape}."
        )
    if frame.dtype != np.uint8:
        raise ValueError(f"The frame must be of type uint8, got {frame.dtype}.")
    if frame.shape[0] == 0 or frame.shape[1] == 0:
        raise ValueError("The frame is empty.")
    return np.ascontiguousarray(frame)


def _clip_box(box: np.ndarray, width: int, height: int) -> tuple[int, int, int, int]:
    """Round a box to integers and move it fully inside the frame.

    MTCNN returns floating point coordinates that can stick out slightly past
    the image border, so the box is clamped before it is used for slicing.
    """
    x1 = int(min(max(round(float(box[0])), 0), width))
    y1 = int(min(max(round(float(box[1])), 0), height))
    x2 = int(min(max(round(float(box[2])), 0), width))
    y2 = int(min(max(round(float(box[3])), 0), height))
    return x1, y1, x2, y2


def detect_faces(frame: np.ndarray) -> list[dict[str, object]]:
    """Detect every face in one image or live webcam frame.

    Arguments:
        frame {np.ndarray} -- an image as returned by OpenCV, i.e. a uint8
            NumPy array of shape (height, width, 3) in BGR order. This is
            exactly what ``VideoCapture.read()`` returns during the real-time
            loop.

    Returns:
        list[dict] -- one dict per detected face, with the keys "box",
        "confidence" and "face" as described in the module docstring. The list
        is empty when the frame contains no face, and also when the detected
        boxes turn out to be invalid or empty once clipped to the frame.

    Example:
    >>> frame = read_image("data/faces/person_01/image01.jpg")
    >>> for face in detect_faces(frame):
    ...     x1, y1, x2, y2 = face["box"]
    ...     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    """
    checked_frame = _check_frame(frame)
    height, width = checked_frame.shape[:2]

    detector = _get_detector()

    # MTCNN normalises the input as (pixel - 127.5) / 128, which assumes the
    # RGB channel order its networks were trained on. OpenCV frames are BGR, so
    # the channels are swapped before detection.
    rgb_frame = cv2.cvtColor(checked_frame, cv2.COLOR_BGR2RGB)

    # MTCNN.detect returns (boxes, probabilities) for a single image, where
    # boxes is None when nothing was detected.
    boxes, probabilities = detector.detect(rgb_frame)
    if boxes is None or len(boxes) == 0:
        return []

    faces: list[dict[str, object]] = []
    for box, probability in zip(boxes, probabilities):
        if probability is None:
            continue

        x1, y1, x2, y2 = _clip_box(box, width, height)
        if x2 <= x1 or y2 <= y1:
            # A degenerate box would give an empty crop, so it is skipped.
            continue

        face = checked_frame[y1:y2, x1:x2]
        if face.size == 0:
            continue

        faces.append(
            {
                "box": (x1, y1, x2, y2),
                "confidence": float(probability),
                "face": face,
            }
        )

    return faces


def _demo(image_path: str | None) -> None:
    """Run the detector on a still image, without needing a webcam."""
    if image_path is None:
        # No test image is bundled with the project, so a blank frame is used
        # to show the normal "no face detected" result instead of failing.
        print("No image path was given, so a blank frame is used.")
        print("Usage: python src/face_detector.py <image_path>")
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
    else:
        frame = read_image(image_path)

    print(f"Frame size: {frame.shape[1]}x{frame.shape[0]} (width x height)")

    detected = detect_faces(frame)
    if not detected:
        print("No face detected.")
        return

    print(f"Detected {len(detected)} face(s):")
    for number, face in enumerate(detected, start=1):
        x1, y1, x2, y2 = face["box"]
        print(
            f"  Face {number}: box=({x1}, {y1}, {x2}, {y2}), "
            f"confidence={face['confidence']:.3f}, "
            f"crop size={face['face'].shape[1]}x{face['face'].shape[0]}"
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _demo(None)
    else:
        try:
            _demo(sys.argv[1])
        except (OSError, ValueError) as error:
            print(f"Could not run the detector: {error}")
