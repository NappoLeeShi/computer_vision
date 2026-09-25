# Step 5 — Integrate the Complete Real-Time Face Recognition Pipeline

Implement the final integration for Practical Assignment 5.

First read and understand:

- README.md
- docs/plan.md
- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- prompts/03_face_matching.md
- prompts/04_webcam.md
- src/face_detector.py
- src/face_embedding.py
- src/face_matching.py
- src/webcam.py
- the lecture material for Practical Assignment 5

Do not implement functionality outside the practical assignment.

## Goal

Implement:

main.py

The final application must perform REAL-TIME face recognition using the physical webcam.

The complete pipeline must be:

Reference images
    ↓
FaceNet
    ↓
Reference embeddings

Physical webcam
    ↓
OpenCV live frame
    ↓
MTCNN
    ↓
Detected face crops
    ↓
FaceNet
    ↓
Live face embeddings
    ↓
Cosine similarity
    ↓
Threshold = 0.7
    ↓
Matched / Unknown
    ↓
Draw result on webcam frame
    ↓
Display live video

## Important distinction

Reference images are stored in:

data/faces/

They are NOT the live input.

The live input MUST come from the physical webcam.

Do not implement an image-folder recognition loop.

Do not replace the webcam with stored images.

## Step 1 — Load reference images

main.py is responsible for preparing the reference embeddings.

The expected directory structure is:

data/faces/
├── person_01/
│   ├── image01.jpg
│   ├── image02.jpg
│   └── image03.jpg
│
└── person_02/
    ├── image01.jpg
    └── image02.jpg

Each subdirectory represents one known identity.

For every identity:

1. Find its reference image files.
2. Load each image.
3. Generate a FaceNet embedding using src/face_embedding.py.
4. Store the embeddings grouped by identity.

The resulting structure should be compatible with face_matching.match_embedding():

{
    "person_01": [embedding1, embedding2, ...],
    "person_02": [embedding1, embedding2, ...]
}

Do not create a database.

Do not create a complicated dataset abstraction.

Keep this logic simple.

## Image loading

Use OpenCV or PIL consistently with the existing embedding interface.

Remember that src/face_embedding.py expects BGR uint8 NumPy images.

Skip unreadable reference images with a clear warning.

Do not silently create an identity with zero embeddings.

If no valid reference images are available, fail clearly with a useful message.

## Step 2 — Initialize models

Reuse the existing modules:

- src/face_detector.py
- src/face_embedding.py
- src/face_matching.py
- src/webcam.py

Do NOT instantiate a second MTCNN model.

Do NOT instantiate a second FaceNet model.

The existing modules already cache/reuse their models.

Do not move model logic into main.py.

## Step 3 — Open the webcam

Use src/webcam.py.

The default camera index should remain configurable.

For example:

python main.py
python main.py --camera 0

If a simple CLI argument system is useful, use argparse.

Do not add a CLI framework.

## Step 4 — Process each live frame

For every webcam frame:

1. Receive the BGR frame from webcam.py.
2. Detect faces using face_detector.detect_faces().
3. For every detected face:
   - get its bounding box
   - get its face crop
   - generate a FaceNet embedding
   - compare it against all reference embeddings
   - obtain label and similarity
4. Draw the result on the frame.
5. Display the frame.

Do not save the webcam frame.

Do not save screenshots.

Do not save video.

## Step 5 — Draw detection results

For every detected face, draw:

- bounding box
- identity label
- similarity score

For example:

person_01 0.91

or:

Unknown 0.62

Use OpenCV drawing functions.

Keep the visualisation simple.

Do not add a GUI framework.

Do not add complicated visual effects.

The final webcam window should clearly show:

- detected face location
- predicted identity
- similarity

## Step 6 — Unknown faces

If face_matching.match_embedding() returns:

{
    "label": "Unknown",
    "similarity": ...
}

display:

Unknown <similarity>

Do not invent an identity.

Do not lower the threshold automatically.

Keep the default threshold at:

0.7

The threshold should be configurable from main.py if practical.

## Step 7 — Multiple faces

The webcam may contain multiple faces.

Process every detected face independently.

For example:

Frame
    ↓
MTCNN detects 3 faces
    ↓
FaceNet generates 3 embeddings
    ↓
Matching produces 3 results
    ↓
Draw 3 bounding boxes and labels

Do not stop after detecting the first face.

## Step 8 — No faces

If MTCNN returns no faces:

- display the original frame
- do not raise an exception
- continue the webcam loop

"No face detected" is a normal real-time condition.

Do not display an Unknown label when no face exists.

## Step 9 — Performance

Keep the real-time loop simple.

Do not:

- reload models per frame
- reload reference images per frame
- regenerate reference embeddings per frame
- create unnecessary objects inside the loop
- save frames
- perform unnecessary image transformations

Reference embeddings must be generated ONCE before entering the webcam loop.

Models must be loaded/reused rather than recreated for every face.

## Step 10 — Webcam lifecycle

Use the cleanup behavior already implemented in src/webcam.py.

When the user presses:

q

the application should:

- stop the loop
- release the webcam
- close OpenCV windows

If an exception occurs, cleanup must still happen.

Do not duplicate webcam lifecycle logic unnecessarily in main.py.

## Step 11 — Console output

Keep console output useful but minimal.

At startup, print something similar to:

Loading reference embeddings...
Loaded identities: person_01, person_02

Starting webcam...

During the webcam loop, do NOT print a message for every frame.

Do not flood the terminal.

## Step 12 — CLI options

Keep command-line options minimal.

At most support:

--camera
--threshold
--data-dir

Example:

python main.py --camera 0 --threshold 0.7 --data-dir data/faces

Defaults:

camera = 0
threshold = 0.7
data directory = data/faces

Do not build a complex command-line interface.

## Step 13 — Error handling

Provide clear errors for:

- data/faces does not exist
- no valid reference images
- unreadable reference image
- webcam cannot be opened
- invalid threshold
- invalid camera index

Do not hide errors.

Do not silently continue with an empty reference database.

## Step 14 — Architecture constraints

main.py is the integration layer.

Do not move existing responsibilities into main.py.

Use the existing module interfaces:

face_detector.py
    → detect_faces(frame)

face_embedding.py
    → generate_embedding(face_image)

face_matching.py
    → match_embedding(query_embedding, reference_embeddings, threshold)

webcam.py
    → webcam lifecycle / frame capture / display

Keep the modules independent.

## Step 15 — Do not add unnecessary functionality

Do NOT implement:

- model training
- Siamese networks
- Triplet Loss
- databases
- REST APIs
- web interfaces
- GUI frameworks
- authentication
- logging frameworks
- multiprocessing
- distributed processing
- persistent user management
- video recording
- screenshot capture

The assignment is a simple real-time FaceNet + MTCNN webcam recognition system.

## Step 16 — Testing

Perform tests in increasing scope.

### Test A — Reference loading

Verify that:

- reference directories are discovered
- images are loaded
- embeddings are generated
- identities are stored correctly

### Test B — Existing modules

Verify that:

- MTCNN detection still works
- FaceNet embedding generation still works
- matching still works

Do not rewrite those modules.

### Test C — Real webcam

Run the actual application with the physical webcam.

Verify:

1. webcam opens
2. live frames are displayed
3. one known person is detected and recognized
4. another known person is recognized if available
5. an unknown person is labeled Unknown
6. multiple faces can be processed
7. no-face frames continue normally
8. q exits correctly
9. webcam and windows are cleaned up

Do not simulate webcam results if a physical webcam is available.

If a physical webcam is unavailable, clearly state that the real-time test could not be performed.

## Step 17 — Performance observation

Measure or report approximate real-time performance if practical.

Do not aggressively optimize.

The goal is to verify that the complete pipeline works.

If the final pipeline is slower than the standalone detector/embedding tests, explain briefly that the complete pipeline includes detection, embedding, matching, and rendering.

## Documentation

Update README.md with a concise section explaining how to run the final application.

Include:

1. Install dependencies.
2. Put reference images into data/faces/.
3. Run main.py.
4. Use the webcam.
5. Press q to exit.

Also update docs/plan.md to mark the implementation steps as completed.

Do not rewrite the entire README.

Keep documentation concise.

## Prompt history

Do NOT modify previous prompt files.

Create this prompt file before executing this task:

prompts/05_main_integration.md

Store this prompt exactly in that file.

The prompt history must remain sequential.

## Final verification

After implementation:

1. Show the final project tree.
2. Show main.py.
3. Explain the complete runtime flow.
4. Confirm that the webcam is the real-time input.
5. Confirm that reference images are loaded only during initialization.
6. Confirm that reference embeddings are generated only once.
7. Confirm that MTCNN detects every face in each live frame.
8. Confirm that FaceNet generates an embedding for each detected face.
9. Confirm that matching uses cosine similarity and threshold 0.7.
10. Confirm that each result is drawn on the live webcam frame.
11. Report the real webcam test results.
12. Do not add any further functionality beyond this practical assignment.