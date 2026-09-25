# Step 3 — Face Matching

Implement the face matching component described in the project architecture.

First read and understand:

- README.md
- docs/plan.md
- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- src/face_detector.py
- src/face_embedding.py
- the lecture material for Practical Assignment 5

Do not implement unrelated parts of the project.

## Goal

Implement:

src/face_matching.py

The purpose of this module is to compare a face embedding generated from a LIVE webcam face with stored reference face embeddings.

The conceptual pipeline is:

reference image
    ↓
FaceNet
    ↓
reference embedding

LIVE webcam face
    ↓
FaceNet
    ↓
live embedding

reference embedding + live embedding
    ↓
similarity
    ↓
threshold
    ↓
Matched / Unknown

## Similarity

The FaceNet implementation from Step 2 returns L2-normalized 512-dimensional embeddings.

Use cosine similarity for comparing embeddings.

Because the embeddings are L2-normalized, cosine similarity can be calculated using their dot product.

Do not re-implement FaceNet.

Do not generate embeddings inside this module.

This module should only operate on embeddings.

## Required interface

Implement a simple function for comparing two embeddings.

For example:

calculate_similarity(embedding1, embedding2) -> float

The function should:

- accept two embeddings
- validate their shapes
- calculate cosine similarity
- return a float

The expected embedding shape is:

(512,)

Do not hard-code unnecessary assumptions beyond what is required by the FaceNet module.

## Matching

Implement a simple function such as:

match_embedding(
    query_embedding,
    reference_embeddings,
    threshold=0.7
)

The function should:

1. Compare the query/live embedding against every reference embedding.
2. Calculate similarity for each reference.
3. Find the reference with the highest similarity.
4. Compare the highest similarity against the threshold.
5. Return the best identity and similarity result.

The reference embeddings should be supplied by the caller.

Do NOT make this module responsible for scanning data/faces/.

The caller will handle loading reference images and associating them with person identities.

## Expected behavior

If:

best_similarity > threshold

return the corresponding known identity as:

Matched

If:

best_similarity < threshold

return:

Unknown

The lecture specifies a similarity threshold of 0.7 for the practical assignment.

Use 0.7 as the default threshold.

However, keep the threshold configurable.

Do not hard-code 0.7 throughout the implementation.

If the similarity is exactly equal to the threshold, choose and document one consistent behavior.

Prefer a simple comparison such as:

similarity >= threshold

for Matched.

## Multiple reference images per person

A person may have multiple reference images.

For example:

person_01:
    embedding_01
    embedding_02
    embedding_03

person_02:
    embedding_01
    embedding_02

The matching function should be able to compare the query embedding against multiple reference embeddings.

Keep the data structure simple.

A suitable structure could be:

{
    "person_01": [embedding1, embedding2, embedding3],
    "person_02": [embedding1, embedding2]
}

For each person, determine that person's best similarity to the query.

Then select the person with the highest overall similarity.

Do not introduce a database.

Do not introduce a complex indexing system.

## Return value

Return enough information for the webcam layer to display the result.

For example:

{
    "label": "person_01" or "Unknown",
    "similarity": 0.91
}

A matched result should contain the identity.

An unknown result should contain "Unknown".

Keep the result simple.

## Input validation

Validate:

- embeddings are NumPy arrays
- embeddings have compatible dimensions
- reference embeddings are not empty
- threshold is in a sensible range
- embeddings do not contain NaN or Inf values

Raise clear ValueError messages for invalid inputs.

Do not silently produce invalid similarity values.

## No reference embeddings

If no reference embeddings are available:

- do not crash unexpectedly
- return a clear error or documented empty/unknown result

Choose the simplest behavior and document it.

## Numerical stability

Use a mathematically correct cosine similarity implementation.

Because Step 2 produces normalized embeddings, avoid unnecessary normalization.

However, the function should still be safe if an embedding has zero norm.

Do not produce NaN.

Handle zero-norm embeddings explicitly.

## Performance

The matching function will eventually be called repeatedly from the live webcam loop.

Keep it lightweight.

Do not load models here.

Do not perform image processing here.

Do not access the webcam here.

Do not generate FaceNet embeddings here.

Only compare already-generated embeddings.

## Documentation

Add concise docstrings/comments explaining:

- what cosine similarity represents
- why embeddings can be compared using dot product
- how the 0.7 threshold is used
- how multiple reference images for one person are handled
- what "Matched" and "Unknown" mean

Keep the explanation appropriate for a university Computer Vision practical.

## Testing

Add small deterministic tests or a __main__ demonstration if useful.

Do not require:

- webcam
- external image files
- model downloads

for the basic matching tests.

Use simple synthetic normalized vectors for testing similarity behavior.

For example, test:

- identical embeddings → high similarity
- clearly different vectors → low similarity
- threshold behavior
- multiple reference embeddings
- Unknown result

Do not use fake test results in the final application.

## Constraints

Do NOT modify:

- src/face_detector.py
- src/face_embedding.py
- src/webcam.py
- main.py

unless a minimal interface adjustment is absolutely necessary.

Do not implement webcam capture yet.

Do not implement the real-time loop yet.

Do not load FaceNet here.

Do not load MTCNN here.

Do not scan data/faces/ here.

Do not add another face recognition model.

Do not train anything.

Keep the implementation simple.

After implementation:

1. Show the resulting src/face_matching.py.
2. Explain the similarity calculation.
3. Explain how multiple reference images are handled.
4. Explain the 0.7 threshold behavior.
5. Show the deterministic test results.
6. Do not proceed to webcam integration.