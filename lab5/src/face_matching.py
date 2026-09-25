"""Face matching against stored reference embeddings.

This module is the decision step of the recognition pipeline. It receives one
embedding coming from a LIVE webcam face, compares it with the embeddings of
the known people, and answers either a known identity or ``"Unknown"``.

    reference image  -> FaceNet -> reference embedding }
                                                  }  -> similarity -> threshold
    LIVE webcam face -> FaceNet -> live embedding   {                          -> label

What cosine similarity means here
---------------------------------
Cosine similarity measures the angle between two vectors rather than their
lengths, so it answers "do these two vectors point in the same direction?".
For face embeddings that means "do these two images look like the same person",
independent of scale. Its value lies in [-1, 1]:

    +1  the vectors point exactly the same way (very likely the same person)
     0  the vectors are perpendicular (no resemblance)
    -1  the vectors point in opposite directions

Why a plain dot product is enough
---------------------------------
FaceNet (see face_embedding.py) returns L2-normalised vectors, so every
embedding has length exactly 1. For two unit vectors the cosine similarity has
a simple form:

    cosine(a, b) = (a . b) / (||a|| * ||b||) = (a . b) / (1 * 1) = a . b

So the similarity is the dot product, with no extra normalisation needed. The
function still divides by the norms when they are not 1, so it stays correct if
it is ever given an un-normalised vector.

How the 0.7 threshold is used
-----------------------------
The lecture for this practical assignment fixes the decision threshold at 0.7:

    similarity >= 0.7  ->  the best matching identity, shown as "Matched"
    similarity <  0.7  ->  "Unknown"

The threshold is a module constant ``DEFAULT_THRESHOLD`` and a parameter of
``match_embedding()``, so it can be changed in one place for experiments. A
similarity exactly equal to the threshold counts as a match, which is the
``>=`` behaviour requested for this step.

What "Matched" and "Unknown" mean
---------------------------------
"Matched" means the face is similar enough to one of the registered people, so
that identity is returned. "Unknown" means no registered person is similar
enough, and it is deliberately returned instead of the closest name: reporting
the nearest identity anyway would produce confident-looking wrong answers.

How multiple reference images per person are handled
-----------------------------------------------------
A person may have several reference photos, so the references are given as a
plain dictionary mapping an identity to a list of embeddings::

    {
        "person_01": [embedding_01, embedding_02, embedding_03],
        "person_02": [embedding_01, embedding_02],
    }

The query embedding is compared with every reference embedding. For each person
the best of their similarities is kept, and the person with the highest of those
best similarities wins. Using the best photo per person is more robust than
averaging, because one photo may be blurred, badly lit or turned away while the
others are fine.

This module only compares embeddings that were already computed. It does not
generate embeddings, does not load FaceNet or MTCNN, does not touch images and
does not scan ``data/faces/``: the caller loads the reference photos, turns them
into embeddings with ``face_embedding.generate_embedding()`` and passes the
resulting dictionary in. That also keeps this module cheap enough to call on
every detected face of every webcam frame.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

import numpy as np


# The similarity threshold given in the lecture for this practical assignment.
DEFAULT_THRESHOLD = 0.7

# FaceNet produces 512-dimensional embeddings (see face_embedding.py). The
# value is not enforced here so the module stays valid for any embedding size
# the FaceNet step may produce.
EMBEDDING_SIZE = 512

UNKNOWN_LABEL = "Unknown"

# Below this distance from 1.0 the norms of two embeddings are treated as
# already normalised, which is the normal case coming out of FaceNet.
UNIT_NORM_TOLERANCE = 1e-6


def _check_embedding(embedding: np.ndarray, name: str) -> np.ndarray:
    """Validate a single embedding and return it as a float array."""
    if not isinstance(embedding, np.ndarray):
        raise ValueError(f"The {name} must be a NumPy array, got {type(embedding)}.")
    if embedding.ndim != 1:
        raise ValueError(
            f"The {name} must be a 1-dimensional array of shape "
            f"({EMBEDDING_SIZE},), got shape {embedding.shape}."
        )
    if embedding.size == 0:
        raise ValueError(f"The {name} is empty.")
    if not np.issubdtype(embedding.dtype, np.floating):
        # Integers are accepted and cast, so a plain list of numbers read from
        # disk does not have to be converted by the caller first.
        embedding = embedding.astype(np.float32)
    if not np.isfinite(embedding).all():
        raise ValueError(f"The {name} contains NaN or Inf values.")
    return embedding


def _check_pair(first: np.ndarray, second: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Validate two embeddings that will be compared with each other."""
    checked_first = _check_embedding(first, "first embedding")
    checked_second = _check_embedding(second, "second embedding")
    if checked_first.shape != checked_second.shape:
        raise ValueError(
            "Both embeddings must have the same number of values, got "
            f"{checked_first.shape[0]} and {checked_second.shape[0]}."
        )
    return checked_first, checked_second


def _check_threshold(threshold: float) -> float:
    """Check that the threshold is a usable cosine similarity value."""
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float, np.floating, np.integer)):
        raise ValueError(
            f"The threshold must be a number, got {type(threshold)}."
        )
    value = float(threshold)
    if not math.isfinite(value):
        raise ValueError("The threshold must be a finite number.")
    if not -1.0 <= value <= 1.0:
        raise ValueError(
            f"The threshold must be within the cosine similarity range "
            f"[-1.0, 1.0], got {value}."
        )
    return value


def _check_reference_embeddings(
    reference_embeddings: Mapping[str, Sequence[np.ndarray] | np.ndarray],
) -> dict[str, list[np.ndarray]]:
    """Check the reference dictionary and return it as identity -> list."""
    if not isinstance(reference_embeddings, Mapping):
        raise ValueError(
            "The reference embeddings must be a dictionary mapping an identity "
            f"to its embeddings, got {type(reference_embeddings)}."
        )
    if len(reference_embeddings) == 0:
        # Raised instead of returning "Unknown", because no references means the
        # caller has not registered anybody yet. That is a setup problem to fix
        # once at start-up, not a per-frame result.
        raise ValueError(
            "No reference embeddings were provided, so no face can be matched."
        )

    checked: dict[str, list[np.ndarray]] = {}
    for identity, embeddings in reference_embeddings.items():
        if not isinstance(identity, str) or not identity:
            raise ValueError(
                f"Every reference identity must be a non-empty string, got {identity!r}."
            )
        if isinstance(embeddings, np.ndarray):
            # A single reference photo is the most common case, so one bare
            # embedding is accepted and wrapped in a list.
            embeddings = [embeddings]
        if isinstance(embeddings, (str, bytes)) or not isinstance(
            embeddings, (Sequence, np.ndarray)
        ):
            raise ValueError(
                f"The embeddings of {identity!r} must be a list of NumPy arrays."
            )
        if len(embeddings) == 0:
            raise ValueError(f"The identity {identity!r} has no embeddings.")

        checked[identity] = [
            _check_embedding(embedding, f"embedding of {identity!r}")
            for embedding in embeddings
        ]

    return checked


def calculate_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Return the cosine similarity of two FaceNet embeddings.

    Arguments:
        embedding1 {np.ndarray} -- a 1-dimensional embedding, normally of shape
            (512,) as produced by ``face_embedding.generate_embedding()``.
        embedding2 {np.ndarray} -- the embedding to compare it with.

    Returns:
        float -- the cosine similarity in [-1.0, 1.0]. Because FaceNet
        embeddings are L2-normalised this is simply the dot product, so no
        renormalisation is done in the normal case.

    Raises:
        ValueError -- if an embedding is not a finite 1-dimensional NumPy
            array, if the two embeddings have different lengths, or if one of
            them has a zero norm, which would make the cosine undefined.

    Example:
    >>> calculate_similarity(embedding_a, embedding_a)
    1.0
    """
    first, second = _check_pair(embedding1, embedding2)

    first_norm = float(np.linalg.norm(first))
    second_norm = float(np.linalg.norm(second))
    if first_norm == 0.0 or second_norm == 0.0:
        raise ValueError(
            "Cosine similarity is undefined for an embedding with a zero norm."
        )

    dot_product = float(np.dot(first, second))
    norm_product = first_norm * second_norm

    # FaceNet already returns unit-length vectors, so the division is skipped
    # unless the norms say otherwise. This keeps the comparison cheap without
    # giving up correctness.
    if math.isclose(norm_product, 1.0, rel_tol=UNIT_NORM_TOLERANCE, abs_tol=0.0):
        return dot_product
    return dot_product / norm_product


def match_embedding(
    query_embedding: np.ndarray,
    reference_embeddings: Mapping[str, Sequence[np.ndarray] | np.ndarray],
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, object]:
    """Match a live face embedding against the registered reference embeddings.

    Arguments:
        query_embedding {np.ndarray} -- the embedding of the face that was just
            detected in a live webcam frame.
        reference_embeddings {dict} -- the known embeddings, as a dictionary
            mapping an identity to a list of embeddings. Several reference
            photos per person are allowed::

                {"person_01": [emb_01, emb_02, emb_03], "person_02": [emb_01]}

        threshold {float} -- the similarity threshold. Above it the identity is
            returned, below it the result is "Unknown". (default: {0.7})

    Returns:
        dict -- ``{"label": ..., "similarity": ...}`` where "label" is the
        identity of the closest person when the best similarity reaches the
        threshold, and ``"Unknown"`` otherwise. "similarity" is the cosine
        similarity that the decision was based on, so the webcam layer can show
        how close the decision was. A similarity exactly equal to the threshold
        counts as a match.

    Raises:
        ValueError -- for any invalid embedding, an empty reference dictionary
            or a threshold outside [-1.0, 1.0].

    Example:
    >>> result = match_embedding(live_embedding, references)
    >>> result["label"] in ("person_01", "Unknown")
    True
    """
    query = _check_embedding(query_embedding, "query embedding")
    references = _check_reference_embeddings(reference_embeddings)
    checked_threshold = _check_threshold(threshold)

    best_label = UNKNOWN_LABEL
    best_similarity = -1.0

    for identity, embeddings in references.items():
        # The best photo of this person decides how well this person matches.
        person_similarity = max(
            calculate_similarity(query, embedding) for embedding in embeddings
        )
        if person_similarity > best_similarity:
            best_similarity = person_similarity
            best_label = identity

    if best_similarity >= checked_threshold:
        return {"label": best_label, "similarity": best_similarity}

    return {"label": UNKNOWN_LABEL, "similarity": best_similarity}


def _unit_vector(angle_degrees: float) -> np.ndarray:
    """Return a deterministic unit vector at the given angle to a fixed base.

    Every vector produced here lies in the same two-dimensional plane and is
    rotated from the same base vector, so the cosine similarity between any two
    of them is exactly the cosine of the difference of their angles. That makes
    the expected result of the demonstration below known in advance.

    Used only by the demonstration; it is not part of the matching logic.
    """
    generator = np.random.default_rng(0)
    base = generator.standard_normal(EMBEDDING_SIZE)
    base /= np.linalg.norm(base)

    axis = np.zeros(EMBEDDING_SIZE)
    axis[0] = 1.0
    sideways = axis - np.dot(axis, base) * base
    sideways /= np.linalg.norm(sideways)

    radians = math.radians(angle_degrees)
    combined = math.cos(radians) * base + math.sin(radians) * sideways
    return (combined / np.linalg.norm(combined)).astype(np.float32)


def _demo() -> None:
    """Run deterministic checks on synthetic embeddings.

    No webcam, no image files and no model download are needed: the behaviour of
    the matching logic is fully determined by the vectors given to it.
    """
    print("=== 1. similarity of known vectors ===")
    base = _unit_vector(0.0)
    for angle in (0, 30, 45, 60, 90, 180):
        similarity = calculate_similarity(base, _unit_vector(float(angle)))
        print(f"  angle {angle:3d} deg -> similarity {similarity:+.4f}")

    print("\n=== 2. threshold behaviour (default 0.7) ===")
    references = {"person_01": [_unit_vector(0.0), _unit_vector(10.0)]}
    for angle in (0, 30, 45, 50, 60, 90):
        result = match_embedding(_unit_vector(angle), references)
        print(
            f"  query at {angle:3d} deg -> label={result['label']:<10s} "
            f"similarity={result['similarity']:.4f}"
        )

    print("\n=== 3. exactly at the threshold counts as Matched ===")
    # The threshold is set to the computed similarity itself, so the >= test is
    # exercised exactly, with no floating point rounding in the way.
    exact_similarity = calculate_similarity(_unit_vector(0.0), _unit_vector(50.0))
    single = {"person_01": [_unit_vector(0.0)]}
    at_threshold = match_embedding(_unit_vector(50.0), single, exact_similarity)
    just_above = match_embedding(
        _unit_vector(50.0), single, math.nextafter(exact_similarity, 1.0)
    )
    print(f"  similarity {exact_similarity:.6f}, threshold set to the same value")
    print(f"    threshold == similarity -> {at_threshold}")
    print(f"    threshold just higher   -> {just_above}")

    print("\n=== 4. several identities, several photos each ===")
    multi = {
        "person_01": [_unit_vector(0.0), _unit_vector(80.0), _unit_vector(85.0)],
        "person_02": [_unit_vector(50.0), _unit_vector(52.0)],
    }
    for angle in (0, 30, 50, 90):
        result = match_embedding(_unit_vector(angle), multi)
        print(
            f"  query at {angle:3d} deg -> label={result['label']:<10s} "
            f"similarity={result['similarity']:.4f}"
        )

    print("\n=== 5. a face of nobody in the references ===")
    result = match_embedding(_unit_vector(180.0), multi)
    print(f"  {result}  (label is {UNKNOWN_LABEL!r})")

    print("\n=== 6. one single photo per person is accepted too ===")
    single_bare = {"person_01": _unit_vector(0.0), "person_02": _unit_vector(90.0)}
    print(f"  query at   0 deg -> {match_embedding(_unit_vector(0.0), single_bare)}")
    print(f"  query at  90 deg -> {match_embedding(_unit_vector(90.0), single_bare)}")

    print("\n=== 7. invalid inputs raise clear errors ===")
    bad_inputs = [
        ("None embedding", None, multi),
        ("2-D embedding", np.zeros((2, 512), np.float32), multi),
        ("length mismatch", _unit_vector(0.0), {"person_01": [np.zeros(256, np.float32)]}),
        ("NaN in embedding", np.full(512, np.nan, np.float32), multi),
        ("Inf in embedding", np.full(512, np.inf, np.float32), multi),
        ("zero-norm embedding", np.zeros(512, np.float32), multi),
        ("empty references", _unit_vector(0.0), {}),
        ("references not a dict", _unit_vector(0.0), [_unit_vector(0.0)]),
        ("empty person list", _unit_vector(0.0), {"person_01": []}),
        ("empty identity name", _unit_vector(0.0), {"": [_unit_vector(0.0)]}),
    ]
    for label, query, refs in bad_inputs:
        try:
            match_embedding(query, refs)
            print(f"  {label:20s} -> no error (unexpected)")
        except ValueError as error:
            print(f"  {label:20s} -> ValueError: {error}")

    for bad_threshold in (1.5, -2.0, float("nan"), "high"):
        try:
            match_embedding(base, multi, threshold=bad_threshold)
            print(f"  threshold {str(bad_threshold):20s} -> no error (unexpected)")
        except ValueError as error:
            print(f"  threshold {str(bad_threshold):20s} -> ValueError: {error}")


if __name__ == "__main__":
    _demo()
