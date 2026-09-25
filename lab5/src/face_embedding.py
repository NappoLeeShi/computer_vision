"""Face embedding with a pre-trained FaceNet model.

What is a FaceNet embedding?
----------------------------
FaceNet is a deep convolutional network pre-trained to map a face image to a
short numerical vector that describes *who* the face belongs to. The network
was trained beforehand on a large face dataset, so this project only uses it
for inference; no training, fine-tuning or triplet/contrastive loss is done
here.

The vector returned by FaceNet here has 512 values. Two images of the same
person end up close to each other in this 512-dimensional space, while images
of different people end up far apart. That is the property the next module
exploits.

Why the same function is used for reference and webcam faces
------------------------------------------------------------
A reference photo and a webcam frame are both just images of a face, so both
go through exactly the same function ``generate_embedding()``. This is the
whole point of using an embedding instead of comparing pixels: both sides of
the comparison are reduced to the same kind of vector by the same model, so the
numbers are directly comparable. If the reference photos and the webcam faces
were processed differently, the resulting vectors would not be comparable and
recognition would fail.

How face_matching.py will use the output
-----------------------------------------
The returned vector is L2-normalised, so its length is exactly 1. Two such
vectors can therefore be compared with a plain dot product, which is the cosine
similarity between them and lies in [-1, 1]. The matching module only has to
compare the live embedding with the reference embeddings and apply the
similarity threshold; it does not need to know anything about FaceNet.

The exact preprocessing below is the one required by this pre-trained model, so
it lives here and not in the face detector.
"""

from __future__ import annotations

import sys

import cv2
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1


DEFAULT_PRETRAINED = "vggface2"

# The pre-trained FaceNet model expects a 160x160 RGB face image and produces
# a 512-dimensional embedding.
INPUT_SIZE = 160
EMBEDDING_SIZE = 512

_model: InceptionResnetV1 | None = None
_device: torch.device | None = None


def _get_device() -> torch.device:
    """Return the device FaceNet runs on: CUDA when present, otherwise CPU.

    A GPU is only used when one is actually detected, so the project still runs
    on an ordinary university computer with no GPU.
    """
    global _device
    if _device is None:
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return _device


def _get_model() -> InceptionResnetV1:
    """Return the shared FaceNet model, loading it on first use.

    Loading the pre-trained weights costs far more than a single inference, so
    the model is created once and reused for every face. The webcam loop calls
    this indirectly many times per second, so reloading the model for each face
    would make real-time recognition impossible.

    On the first call the pre-trained VGGFace2 weights (~107 MB) are downloaded
    once and then read from the local torch cache on every later run.
    """
    global _model
    if _model is None:
        model = InceptionResnetV1(
            pretrained=DEFAULT_PRETRAINED,
            classify=False,
            device=_get_device(),
        )
        # eval() switches off dropout and freezes the batch-norm statistics, so
        # the same face always produces the same embedding.
        model.eval()
        _model = model
    return _model


def _check_face_image(face_image: np.ndarray) -> np.ndarray:
    """Validate a face image and return it as a contiguous BGR array.

    The expected input is the same kind of array OpenCV produces, because that
    is what the webcam and the face detector both provide.
    """
    if not isinstance(face_image, np.ndarray):
        raise ValueError(
            "The face image must be a NumPy array as returned by OpenCV."
        )
    if face_image.ndim != 3 or face_image.shape[2] != 3:
        raise ValueError(
            f"The face image must have shape (height, width, 3), "
            f"got {face_image.shape}."
        )
    if face_image.dtype != np.uint8:
        raise ValueError(
            f"The face image must be of type uint8, got {face_image.dtype}."
        )
    if face_image.shape[0] == 0 or face_image.shape[1] == 0:
        raise ValueError("The face image is empty.")
    return np.ascontiguousarray(face_image)


def _preprocess(face_image: np.ndarray) -> torch.Tensor:
    """Turn one BGR face image into the 1x3x160x160 tensor FaceNet expects.

    The three steps are the preprocessing required by the pre-trained model:

        1. Colour: the model was trained on RGB images, but OpenCV hands out
           BGR, so the red and blue channels are swapped.
        2. Size: the model only accepts a 160x160 square image, so the face is
           resized. This is what replaces the resizing the detector
           deliberately leaves out.
        3. Normalisation: pixel values are mapped from [0, 255] to about
           [-1, 1] with (pixel - 127.5) / 128, which is the scaling this
           pre-trained model expects. A batch dimension of 1 is added because
           the model works on batches of images.
    """
    checked_image = _check_face_image(face_image)

    rgb_image = cv2.cvtColor(checked_image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(
        rgb_image, (INPUT_SIZE, INPUT_SIZE), interpolation=cv2.INTER_AREA
    )

    normalised = (resized_image.astype(np.float32) - 127.5) / 128.0

    # HWC (height, width, channel) becomes the NCHW layout the model expects.
    tensor = torch.from_numpy(np.ascontiguousarray(normalised))
    return tensor.permute(2, 0, 1).unsqueeze(0).to(_get_device())


def generate_embedding(face_image: np.ndarray) -> np.ndarray:
    """Return the FaceNet embedding of one face image.

    Arguments:
        face_image {np.ndarray} -- a face image as a uint8 NumPy array of shape
            (height, width, 3) in BGR order. That covers all three sources used
            in this project: face crops from the webcam produced by
            ``face_detector.detect_faces()``, and reference photos from
            ``data/faces/`` loaded with OpenCV.

    Returns:
        np.ndarray -- one embedding vector of shape (512,) and dtype float32.
        The vector is L2-normalised, so its Euclidean length is 1 and a dot
        product between two embeddings is their cosine similarity.

    Raises:
        ValueError -- if the input is not a usable uint8 BGR image.

    Example:
    >>> frame = read_image("data/faces/person_01/image01.jpg")
    >>> faces = detect_faces(frame)
    >>> embedding = generate_embedding(faces[0]["face"])
    >>> embedding.shape
    (512,)
    """
    model = _get_model()
    face_tensor = _preprocess(face_image)

    with torch.no_grad():
        embedding = model(face_tensor)

    # The model already L2-normalises its output, so no further transformation
    # is applied here; only the leading batch dimension is removed.
    return embedding[0].cpu().numpy().astype(np.float32)


def _demo(image_path: str | None) -> None:
    """Embed the first face found in a still image, without needing a webcam."""
    if image_path is None:
        # No test image is bundled with the project, so the usage example is
        # printed instead of failing.
        print("No image path was given, so no embedding is computed.")
        print("Usage: python src/face_embedding.py <image_path>")
        print()
        print("Example:")
        print('    frame = cv2.imread("data/faces/person_01/image01.jpg")')
        print("    for face in detect_faces(frame):")
        print("        embedding = generate_embedding(face['face'])")
        return

    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"Could not read the image: {image_path}")

    from face_detector import detect_faces

    faces = detect_faces(frame)
    if not faces:
        print(f"No face detected in {image_path}.")
        return

    embedding = generate_embedding(faces[0]["face"])
    print(f"Image: {image_path}")
    print(f"Faces detected: {len(faces)}")
    print(f"Embedding shape: {embedding.shape}, dtype: {embedding.dtype}")
    print(f"Embedding L2 norm: {float(np.linalg.norm(embedding)):.6f}")
    print(f"First 8 values: {np.array2string(embedding[:8], precision=4)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _demo(None)
    else:
        try:
            _demo(sys.argv[1])
        except (OSError, ValueError) as error:
            print(f"Could not compute the embedding: {error}")
