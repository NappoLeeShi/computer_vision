# Step 1 — Face Detection with MTCNN

Implement the face detection component described in this project architecture.

First read and understand:

- README.md
- docs/plan.md
- prompts/00_project_architecture.md
- the lecture material available for this practical assignment

Do not implement unrelated parts of the project yet.

## Goal

Implement:

src/face_detector.py

The purpose of this module is to detect faces from images or live webcam frames using MTCNN.

The final application will use this module on LIVE webcam frames.

The expected pipeline is:

Webcam frame
    ↓
MTCNN
    ↓
Detected face bounding boxes
    ↓
Face crops
    ↓
Face embedding module

## Requirements

1. Use MTCNN for face detection.

2. The implementation should provide a simple interface that can receive an image/frame and return detected faces.

3. Each detected face should provide enough information for the next stage, including:
   - bounding box
   - face image/crop
   - detection confidence if available

4. The module should support multiple faces in a single frame.

5. Do not implement FaceNet embedding generation yet.

6. Do not implement face matching yet.

7. Do not implement webcam capture yet.

8. Do not implement the main real-time loop yet.

9. Keep the implementation simple and easy to explain.

## Face crop

For each detected face:

- extract the corresponding face region from the input frame
- make sure the crop coordinates stay inside the image boundaries
- ignore invalid or empty face crops

Do not perform unnecessary image processing.

Do not resize the face for FaceNet inside this module unless the selected MTCNN implementation requires it.

If preprocessing is required specifically by the selected MTCNN implementation, keep it minimal and document it.

## Multiple faces

The detector should return a list of detected faces.

Conceptually:

[
    {
        "box": ...,
        "confidence": ...,
        "face": ...
    },
    ...
]

Use a simple data structure.

Do not create unnecessary classes.

## Webcam compatibility

The detector must work with frames returned by OpenCV.

OpenCV frames are normally NumPy arrays in BGR format.

Handle the required color conversion correctly for the selected MTCNN implementation.

Do not open the webcam from this module.

The webcam module is responsible for webcam access.

## Error handling

Handle:

- invalid input frames
- no detected faces
- invalid bounding boxes

"No face detected" should be a normal result, not an exception.

## Dependencies

Use only the dependencies required for MTCNN and the image/frame processing.

Do not add unrelated libraries.

Do not install or introduce another face detector such as:
- Haar Cascade
- YOLO
- RetinaFace
- dlib face detector

The practical assignment specifically requires MTCNN.

## Testing

Add a small test/demo section if useful.

The test must NOT require a webcam.

Do not invent test images.

If no test image is available, provide a clear usage example instead of failing.

## Documentation

Add concise docstrings/comments explaining:

- what MTCNN does
- what the returned bounding box represents
- what the confidence score represents
- how the detected face crop will be used by the FaceNet stage

Keep the explanation at the level appropriate for a university Computer Vision practical.

## Constraints

Do NOT modify:

- src/face_embedding.py
- src/face_matching.py
- src/webcam.py
- main.py

unless a minimal import/interface adjustment is absolutely necessary.

Do not implement the rest of the pipeline.

After implementation:

1. Show the resulting src/face_detector.py.
2. Explain briefly how MTCNN is used.
3. Explain the input/output interface of the module.
4. Verify that the module is ready to receive live OpenCV webcam frames later.
5. Do not proceed to the next step.