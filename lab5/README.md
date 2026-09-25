# Real-time Face Recognition with FaceNet & MTCNN on Webcam

A simple Computer Vision practical assignment that recognises known people in a **live webcam stream**.

## Purpose

The system registers a few reference photos of known people, then points the camera at a face and decides in real time whether that person is known. The recognition is performed on live frames only, not on a folder of images.

The pipeline is implemented and runs against the physical webcam.

## Real-time pipeline

```
Webcam
  -> OpenCV captures live frames
  -> MTCNN detects faces
  -> FaceNet generates face embeddings
  -> Live embedding is compared with reference embeddings
  -> Similarity threshold is applied
  -> "Matched" / "Unknown" is displayed on the frame
```

The loop runs continuously until the user presses `q` in the video window.

## Roles in the pipeline

- **Reference images** (`data/faces/`): photos of the people to recognise, grouped per person. They are used **only** to build reference embeddings, never as live input.
- **MTCNN** (`src/face_detector.py`): finds the face regions in each webcam frame, so recognition only works on faces, not on the whole scene.
- **FaceNet** (`src/face_embedding.py`): a pre-trained model that turns each detected face into a compact numerical vector. The model is used as-is and never trained.
- **Embedding comparison** (`src/face_matching.py`): measures how close the live embedding is to the stored reference embeddings.
- **Similarity threshold**: a configurable cut-off. `similarity >= 0.7` gives the matched identity, `similarity < 0.7` gives `Unknown`. Anything below the threshold is rejected instead of being forced into a name.

## Project structure

- `main.py`: the complete real-time loop, wiring the four modules together.
- `src/face_detector.py`: MTCNN face detection.
- `src/face_embedding.py`: pre-trained FaceNet embedding generation.
- `src/face_matching.py`: embedding comparison and threshold decision.
- `src/webcam.py`: OpenCV webcam capture, display and exit handling.
- `data/faces/`: reference images of known people, one folder per person. Webcam frames are never stored here.
- `results/embeddings/`: optional storage for reference embeddings. Webcam frames are never stored here.
- `docs/plan.md`: implementation plan.
- `prompts/00_project_architecture.md`: the instruction used to create this structure.

## Running the project

1. **Install the dependencies:**

   ```bash
   python -m venv .venv
   .venv/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   .venv/bin/pip install -r requirements.txt
   ```

   On Python 3.14 the pinned transitive dependencies of `facenet-pytorch` are
   outdated, so install the last line with `--no-deps` after `torch` is in place:
   `.venv/bin/pip install --no-deps facenet-pytorch requests tqdm`

2. **Add reference images.** Put one subfolder per person in `data/faces/`, with
   one or more clear, front-facing photos inside it, for example
   `data/faces/person_01/photo01.jpg`. A subfolder with no readable face is
   skipped with a warning, and starting with no usable photo at all is an error.
   Webcam frames are never written into this folder.

3. **Run the application** from the project root:

   ```bash
   .venv/bin/python main.py
   ```

   Optional flags: `--camera N` (webcam index, default `0`),
   `--threshold F` (default `0.7`), `--data-dir PATH` (default `data/faces`).

4. **Use the webcam.** Reference embeddings are built once at start-up, then the
   live loop runs: each frame is scanned by MTCNN, every detected face is turned
   into a FaceNet embedding and compared with the references. A matched face is
   drawn in green with its name and similarity, an unmatched one in red as
   `Unknown`. A frame with no face is shown untouched and the loop continues.

5. **Press `q`** in the video window to exit and release the camera.
