# Step 4 — Real-Time Webcam Capture

Implement the webcam component described in the project architecture.

First read and understand:

- README.md
- docs/plan.md
- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- prompts/03_face_matching.md
- src/face_detector.py
- src/face_embedding.py
- src/face_matching.py
- the lecture material for Practical Assignment 5

Do not implement unrelated parts of the project.

## Goal

Implement:

src/webcam.py

The purpose of this module is to provide a simple real-time webcam interface using OpenCV.

The physical webcam must be the LIVE input source.

The module should provide the infrastructure needed for the final pipeline:

Physical webcam
    ↓
OpenCV VideoCapture
    ↓
live BGR frame
    ↓
face detection
    ↓
face embedding
    ↓
face matching

However, do NOT integrate MTCNN, FaceNet, or face matching into this module yet.

Those responsibilities belong to their existing modules.

## Webcam requirements

Use OpenCV VideoCapture.

The module should:

1. Open the default webcam.
2. Continuously read frames.
3. Return/provide frames in the normal OpenCV BGR NumPy format.
4. Detect when a frame cannot be read.
5. Release the webcam cleanly.
6. Destroy OpenCV windows when the webcam session ends.

The default camera index should be configurable.

For example:

camera_index = 0

Do not hard-code camera index 0 throughout the implementation.

## Keep responsibilities separate

webcam.py is responsible ONLY for:

- opening the webcam
- reading frames
- handling camera lifecycle
- displaying frames if a simple display helper is provided
- detecting the exit key
- releasing the camera

Do NOT put the following into webcam.py:

- MTCNN
- FaceNet
- face embeddings
- cosine similarity
- matching
- threshold decisions
- identity recognition

Those will be integrated later by main.py.

## API

Provide a simple interface suitable for the final real-time application.

For example, a function such as:

open_webcam(camera_index=0)

or a small set of simple functions for:

- opening the camera
- reading a frame
- releasing the camera

Keep the interface simple.

Do not create unnecessary classes unless OpenCV's resource lifecycle clearly benefits from one.

## Frame handling

Frames returned from OpenCV should remain:

- NumPy arrays
- BGR format
- shape (height, width, 3)

Do not resize frames in this module.

Do not convert BGR to RGB here.

The face detector already handles the color conversion required by MTCNN.

Do not perform face preprocessing here.

## Real-time behavior

The implementation should support a continuous loop.

The final application will eventually do:

while webcam is running:
    read frame
    process frame
    display frame
    check exit key

However, do not implement the complete face-recognition pipeline in this step.

Only implement the webcam-side loop/infrastructure.

## Exit behavior

Use a simple keyboard command to exit the webcam session.

Use:

q

as the default exit key.

The exit key should be configurable if practical.

When the user exits:

- release the camera
- destroy OpenCV windows

Make sure cleanup also happens if an exception occurs during the webcam loop.

## Camera errors

Handle:

- camera cannot be opened
- frame cannot be read
- camera becomes unavailable

Provide clear error messages.

Do not silently continue forever if the camera cannot be opened.

## Display

If a simple display helper is implemented, use OpenCV's:

cv2.imshow()

Do not add a GUI framework.

The final application will eventually draw face boxes and recognition results on the frame, but that will be handled during the final integration step.

For this step, a simple raw-frame display/test is sufficient.

## Testing

Provide a simple webcam test/demo if appropriate.

The test should:

1. Open the default webcam.
2. Display the live frames.
3. Exit when q is pressed.
4. Release the camera correctly.

Do not perform face detection, FaceNet inference, or face matching during this test.

Clearly document that this is only a webcam capture test.

If no webcam is available in the current environment, do not fabricate a successful webcam test.

The module should still be implemented correctly.

## Performance

Do not add unnecessary processing to the webcam capture loop.

The goal is to provide frames efficiently to the later recognition pipeline.

Do not resize, encode, save, or preprocess frames unnecessarily.

## Documentation

Add concise docstrings/comments explaining:

- why OpenCV VideoCapture is used
- what format the returned frame uses
- how the webcam lifecycle is handled
- how the final recognition pipeline will consume the frames

Keep the explanation appropriate for a university Computer Vision practical.

## Constraints

Do NOT modify:

- src/face_detector.py
- src/face_embedding.py
- src/face_matching.py
- main.py

unless a minimal interface adjustment is absolutely necessary.

Do not integrate the recognition pipeline yet.

Do not load MTCNN.

Do not load FaceNet.

Do not calculate embeddings.

Do not calculate similarity.

Do not apply the 0.7 threshold.

Do not identify people.

Do not save webcam frames.

Do not add a GUI framework.

Do not add unnecessary dependencies.

After implementation:

1. Show the resulting src/webcam.py.
2. Explain the webcam API.
3. Explain the frame format.
4. Explain the camera cleanup behavior.
5. Show the webcam test result if a physical webcam is available.
6. If webcam testing is unavailable, clearly state that it could not be tested.
7. Do not proceed to main.py integration.