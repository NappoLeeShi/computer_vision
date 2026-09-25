# Step 2 — Face Embedding with FaceNet

Implement the face embedding component described in the project architecture.

First read and understand:

- README.md
- docs/plan.md
- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- src/face_detector.py
- the lecture material for Practical Assignment 5

Do not implement unrelated parts of the project.

## Goal

Implement:

src/face_embedding.py

The purpose of this module is to generate numerical face embeddings using a pre-trained FaceNet model.

The pipeline should be:

face image
    ↓
FaceNet
    ↓
face embedding vector
    ↓
face matching module

The same embedding procedure must be usable for:

1. Reference face images from data/faces/
2. Face crops produced from live webcam frames by face_detector.py

## Model

Use a PRE-TRAINED FaceNet implementation.

Do NOT train FaceNet.

Do NOT implement:
- CNN training
- Siamese network training
- Triplet Loss training
- contrastive learning
- fine-tuning

Reuse the FaceNet implementation/dependencies already selected in Step 1.

Do not introduce a second FaceNet implementation.

## Input

Implement a simple function that accepts a face image as a NumPy array.

The expected input should be compatible with:

- OpenCV webcam face crops
- face crops returned by src/face_detector.py
- reference images loaded from data/faces/

The current face detector returns BGR NumPy image crops.

Handle the required color conversion and preprocessing inside this module.

Do not move FaceNet-specific preprocessing into face_detector.py.

## Output

Return a numerical embedding vector for the input face.

The output should be a NumPy array with a consistent shape and dtype.

The embedding representation must be suitable for similarity comparison in the next module.

Keep the interface simple.

For example:

generate_embedding(face_image) -> np.ndarray

Do not create unnecessary classes.

## Model loading

The FaceNet model should be loaded once and reused.

Do NOT reload the model every time generate_embedding() is called.

This is important because the final application will process many faces from a live webcam stream.

Use a simple module-level or cached model initialization approach.

## Device

Prefer CPU by default unless an available device can be safely detected.

The project must remain usable on a normal university computer without requiring a GPU.

Do not make CUDA mandatory.

If GPU support is available, it may be used, but CPU must remain a valid fallback.

## Preprocessing

Apply the preprocessing required by the selected pre-trained FaceNet implementation.

Do not invent a custom preprocessing pipeline.

Keep preprocessing inside face_embedding.py.

Document briefly:

- expected input color format
- image resizing/alignment requirements
- normalization performed before FaceNet inference

## Embedding normalization

If the selected FaceNet implementation normally uses L2-normalized embeddings for face comparison, preserve that behavior.

Do not add unnecessary transformations to the embedding.

The output should be deterministic for the same input image and model configuration.

## Batch support

A simple single-image function is sufficient for this practical.

Do not build a complex batch-processing framework.

If batch processing is naturally supported by the selected library, keep the implementation simple.

## Reference embeddings

The module should support generating embeddings from reference images, but it should NOT be responsible for scanning the entire data/faces directory yet.

That dataset-loading logic will be handled by the integration layer later.

Keep this module focused on:

image → embedding

## Error handling

Handle invalid inputs clearly.

Examples:

- None
- empty image
- invalid NumPy shape
- unsupported image format/type

Raise clear ValueError messages when appropriate.

Do not silently return fake embeddings.

## Testing

Add a small test/demo section if useful.

Do not require a webcam for testing.

Do not invent test images.

If no test image is available, provide a clear usage example instead.

## Performance

The model must be initialized once and reused.

Do not reload FaceNet for every webcam frame or every detected face.

The final real-time pipeline will depend on this behavior.

## Documentation

Add concise docstrings/comments explaining:

- what a FaceNet embedding represents
- why the same embedding function is used for reference and webcam faces
- what the output vector represents
- how the embedding will be used by face_matching.py

Keep explanations at the level appropriate for a university Computer Vision practical.

## Constraints

Do NOT modify:

- src/face_detector.py
- src/face_matching.py
- src/webcam.py
- main.py

unless a minimal import/interface adjustment is absolutely necessary.

Do not implement face matching yet.

Do not implement webcam capture yet.

Do not implement the final real-time loop yet.

Do not add another face detector.

Do not add another face recognition model.

Do not train any model.

After implementation:

1. Show the resulting src/face_embedding.py.
2. Explain which pre-trained FaceNet implementation is being used.
3. Explain the input/output interface.
4. Explain the preprocessing applied before inference.
5. Verify that the model is loaded once and reused.
6. Verify that CPU execution is supported.
7. Do not proceed to the next step.