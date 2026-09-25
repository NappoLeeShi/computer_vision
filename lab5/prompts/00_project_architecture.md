Create the initial project structure for Practical Assignment 5 based strictly on the lecture material.

The practical assignment is:

"Real-time Face Recognition with FaceNet & MTCNN on Webcam"

The core workflow is:

Webcam
→ OpenCV captures live frames
→ MTCNN detects faces
→ FaceNet generates face embeddings
→ Compare the live embedding with reference embeddings
→ Apply a similarity threshold
→ Display "Matched" or "Unknown"

The webcam must be the LIVE input during recognition.

Do NOT implement the actual recognition algorithm yet.

Create this project structure:

```
lab5/
├── README.md
│
├── prompts/
│   └── 00_project_architecture.md
│
├── data/
│   └── faces/
│       ├── person_01/
│       └── person_02/
│
├── src/
│   ├── face_detector.py
│   ├── face_embedding.py
│   ├── face_matching.py
│   └── webcam.py
│
├── results/
│   └── embeddings/
│
├── docs/
│   └── plan.md
│
├── requirements.txt
│
└── main.py
```

## Responsibilities

### data/faces/

This directory contains REFERENCE images of known people.

Example:

```
data/faces/
├── person_01/
│   ├── image01.jpg
│   ├── image02.jpg
│   └── image03.jpg
│
└── person_02/
    ├── image01.jpg
    ├── image02.jpg
    └── image03.jpg
```

These images are NOT the live recognition input.

They are only used to create reference face embeddings for known people.

Do not store webcam frames here.

### src/face_detector.py

Responsible for face detection using MTCNN.

It will later receive images/frames and return detected face regions.

### src/face_embedding.py

Responsible for generating face embeddings using a pre-trained FaceNet model.

Do NOT train FaceNet from scratch.

The module should later support generating embeddings for both:

* reference images
* faces detected from live webcam frames

### src/face_matching.py

Responsible for:

* comparing a live face embedding with reference embeddings
* calculating the similarity measure
* applying the similarity threshold
* returning the predicted identity or "Unknown"

The lecture specifies:

* similarity > 0.7 → Matched
* similarity < 0.7 → Unknown

Keep the threshold configurable.

Do not implement this logic yet.

### src/webcam.py

Responsible for accessing the physical webcam using OpenCV.

The webcam is the LIVE input source for the recognition system.

It should later:

* open the webcam
* continuously capture frames
* provide frames to the face detection pipeline
* display the processed frames
* allow the user to exit the webcam loop

Do not use a folder of images as a substitute for the webcam.

Do not save webcam frames unless explicitly required later.

### results/embeddings/

Used to store reference embeddings if the final implementation chooses to persist them.

Do not store live webcam frames here.

### main.py

This will later integrate the complete real-time pipeline:

1. Load/create reference embeddings from data/faces/.
2. Open the webcam.
3. Capture live frames.
4. Detect faces using MTCNN.
5. Generate FaceNet embeddings for detected faces.
6. Compare them with reference embeddings.
7. Apply the similarity threshold.
8. Display the identity and similarity result directly on the webcam frame.
9. Continue until the user exits.

The webcam processing must happen continuously in a real-time loop.

### docs/plan.md

Contain a short implementation plan for the practical assignment.

### README.md

Briefly explain:

* project purpose
* real-time webcam recognition pipeline
* role of reference images
* role of MTCNN
* role of FaceNet
* role of embedding comparison
* role of the similarity threshold

Keep it concise.

### prompts/00_project_architecture.md

Store this complete prompt in this file.

### requirements.txt

Only list dependencies that are clearly required by the planned implementation.

Do NOT install unnecessary libraries at this stage.

If the exact FaceNet/MTCNN package choice is not yet determined, do not invent a large dependency list. Leave only clearly justified dependencies for now.

## Important constraints

Keep the project simple and within the scope of the practical assignment.

Do NOT:

* train FaceNet
* implement Siamese network training
* implement Triplet Loss training
* build a CNN from scratch
* add a database
* add a web application
* add a GUI framework
* add unnecessary abstractions
* add unnecessary modules
* create a batch image-recognition pipeline instead of webcam recognition
* save webcam frames unnecessarily

Use a pre-trained FaceNet model.

The final application must perform REAL-TIME recognition from the physical webcam.

For this step, only create the architecture and placeholder files.

Do not implement MTCNN, FaceNet, embedding comparison, or webcam recognition yet.

After creating the structure:

1. Show the final directory tree.
2. Briefly explain the responsibility of each file.
3. Do not proceed to implementation.
