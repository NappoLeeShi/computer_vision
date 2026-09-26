# Lab 5 Session: Prompts and Responses

Exported from opencode session `ses_f26ca8d17ffeAJNSpfElypdpOn` (slug `quiet-moon`, v1.18.18).

| | |
|---|---|
| Session title | Lab 5 Webcam Face Recognition Structure |
| Working directory | `/mnt/E/Projects/computer_vision/lab5` |
| Model | opencode/big-pickle |
| Started | 2026-09-25 22:35 |
| Last activity | 2026-09-25 23:22 |
| Prompts in this document | 7 |

Each section below is one user prompt followed by every assistant text message
produced in response to it, in chronological order.

---

## Prompt 1

*2026-09-25 22:35*

**Prompt**

```text
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

## Responsibilities

### data/faces/

This directory contains REFERENCE images of known people.

Example:

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
```

**Response**

I'll explore the workspace first to understand existing conventions, then create the structure.

Conventions noted (lab4 style: docstring placeholders, concise README). Creating the structure.

Structure created in `/mnt/E/Projects/computer_vision/lab5`.

```
lab5/
├── README.md
├── prompts/
│   └── 00_project_architecture.md
├── data/
│   └── faces/
│       ├── person_01/   (.gitkeep)
│       └── person_02/   (.gitkeep)
├── src/
│   ├── face_detector.py
│   ├── face_embedding.py
│   ├── face_matching.py
│   └── webcam.py
├── results/
│   └── embeddings/      (.gitkeep)
├── docs/
│   └── plan.md
├── requirements.txt
└── main.py
```

**Responsibilities**

| Path | Purpose |
|---|---|
| `README.md` | Concise overview: purpose, webcam pipeline, roles of reference images / MTCNN / FaceNet / comparison / threshold. |
| `prompts/00_project_architecture.md` | The full architecture prompt verbatim. |
| `data/faces/person_01,02/` | Reference photos of known people, one folder per person. Reference embeddings only — never webcam frames, never live input. |
| `src/face_detector.py` | Placeholder docstring: future MTCNN detection of face regions in images and live frames. |
| `src/face_embedding.py` | Placeholder docstring: future pre-trained FaceNet embeddings for both reference images and webcam faces. |
| `src/face_matching.py` | Placeholder docstring: future similarity comparison, configurable threshold (0.7 → Matched / Unknown), identity output. |
| `src/webcam.py` | Placeholder docstring: future OpenCV live capture, frame streaming, display, user exit. No folder-of-images substitute. |
| `results/embeddings/` | Optional persistence of reference embeddings only. |
| `docs/plan.md` | Short implementation plan, written in Vietnamese to match `lab4/docs/plan.md`. |
| `requirements.txt` | Only `numpy` and `opencv-python`, plus a note that the FaceNet/MTCNN package is still undecided. |
| `main.py` | Placeholder docstring: future 9-step real-time integration loop. |

Two things to confirm: I followed lab4's convention of a Vietnamese `plan.md` with the same member table (Thuận = structure, Tiến = implementation, marked *not started*). Also, all source files are docstring-only and pass `py_compile`; nothing is implemented, and I did not install anything.

---

## Prompt 2

*2026-09-25 22:47*

**Prompt**

```text
Read the following project files first:

- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- README.md
- docs/plan.md

Then implement exactly the task described in:

prompts/01_face_detection.md

Do not add functionality beyond that prompt.

After implementation, show me the changes and wait for my review.
```

**Response**

I'll read the referenced files first.

MTCNN isn't installed yet. Installing CPU-only torch + facenet-pytorch (which ships MTCNN) into the project venv so I can actually verify the module runs.

MTCNN works via `facenet-pytorch` (bundled P/R/O-Net weights, no download). Now writing the module.

Now verifying it actually runs — first the no-face path, then a real face from images already in the repo.

`detailed.jpg` has 3 faces — good multi-face test. Running the actual module:

Now updating `requirements.txt` to reflect the packages actually used.

Implemented. Here is the resulting `src/face_detector.py`:

### 1. Resulting `src/face_detector.py`

Shown above (211 lines). Also changed: `requirements.txt` only. `face_embedding.py`, `face_matching.py`, `webcam.py` and `main.py` are untouched.

### 2. How MTCNN is used

`facenet-pytorch` is the MTCNN implementation. It ships the pre-trained P-Net/R-Net/O-Net weights inside the package, so no model download or training happens. The module calls `MTCNN.detect(frame)`, which returns every candidate box surviving the three-stage cascade plus O-Net's score. The detector object is built once in `_get_detector()` (face_detector.py:54) and reused, because reloading the nets each frame would be far too slow for a real-time loop.

One preprocessing step was unavoidable and is documented in the code: MTCNN normalises as `(pixel - 127.5) / 128`, which assumes the **RGB** order its weights were trained on, while OpenCV produces **BGR**. So `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` runs before detection, and the returned crops are taken from the original BGR frame.

### 3. Input / output interface

- **In:** `detect_faces(frame)` — one `uint8` NumPy array of shape `(height, width, 3)` in BGR, i.e. exactly what `VideoCapture.read()` returns. Invalid input raises `ValueError` (wrong type, wrong shape, wrong dtype, empty frame).
- **Out:** `list[dict]`, one entry per face: `"box"` = `(x1, y1, x2, y2)` integer pixel corners, `"confidence"` = float in [0, 1] from O-Net, `"face"` = the crop as a BGR NumPy array. Multiple faces per frame are all returned. **No face → empty list, not an exception.**

Crops come back at original scale with no resizing or extra processing; converting them for FaceNet is the embedding module's job. Boxes are clamped into the frame first (face_detector.py:101), and degenerate/empty crops are skipped.

### 4. Webcam readiness — verified

| Check | Result |
|---|---|
| `datatest/detailed.jpg` (3 faces) | 3 faces, confidences 0.721 / 0.729 / 0.842 |
| `datatest/test.jpg` (1 face) | 1 face, confidence 0.999 |
| Crop correctness | byte-identical to `frame[y1:y2, x1:x2]`; crop re-detects as a face |
| BGR→RGB direction | RGB scores higher than BGR on real faces (0.999 vs 0.998) |
| Box clipping | out-of-range and inverted boxes stay inside the frame |
| Invalid inputs | all 5 malformed cases raise `ValueError` |
| Blank frame / 640×480 frame | `[]` — no exception |
| Non-contiguous frame | handled via `ascontiguousarray` |
| Speed, 640×480, CPU | **64 ms/frame ≈ 15.5 FPS** (1.6 FPS at 1960×1960) |

15.5 FPS on CPU is enough for a real-time webcam loop at 640×480. The module never opens the webcam itself, matching the prompt.

### 5. Dependencies

`requirements.txt` now lists numpy, opencv-python, facenet-pytorch, torch, torchvision, Pillow, requests, tqdm, plus the exact install commands. One thing worth flagging: **`pip install -r requirements.txt` does not work as-is.** facenet-pytorch 2.6.0 still pins `numpy<2`, `Pillow<10.3`, `torch<2.3`, `torchvision<0.18`, and none of those ship Python 3.14 wheels — pip fails building Pillow from source. I installed with:

```
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install --no-deps facenet-pytorch requests tqdm
```

This is documented in `requirements.txt`. I did not proceed to the next step — waiting for your review.

---

## Prompt 3

*2026-09-25 22:59*

**Prompt**

```text
Read and understand:

- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- src/face_detector.py
- README.md
- docs/plan.md

Then implement exactly the task described in:

prompts/02_face_embedding.md

Do not add functionality beyond that prompt.

After implementation, show me:
1. The changes made.
2. The FaceNet model/library selected.
3. The input/output interface.
4. The verification results.

Do not proceed to face matching or webcam integration yet.
```

**Response**

Already read `00_project_architecture.md`, `01_face_detection.md`, `README.md`, `docs/plan.md` this session. Now checking the FaceNet model's own preprocessing contract:

Model loads and outputs L2-normalized 512-d vectors. Now writing the module:

Now full verification:

Same-vs-different separation works, but let me check the realistic case (two MTCNN crops of the same person) against the lecture's 0.7 threshold:

Implemented `src/face_embedding.py` (211 lines). Only that one file changed — `face_detector.py`, `face_matching.py`, `webcam.py`, `main.py` and `requirements.txt` are untouched (no new dependency was needed; `facenet-pytorch` already provides FaceNet).

### 1. Changes made

New file `src/face_embedding.py`. The public surface:

| Symbol | Role |
|---|---|
| `generate_embedding(face_image)` | the one public function: face image → `(512,)` float32 vector |
| `read_image` / `_check_face_image` | input validation → `ValueError` |
| `_preprocess` | the model's required BGR→RGB, resize, normalise steps |
| `_get_model` / `_get_device` | module-level cache; model loaded **once** |

Everything else (docstrings, the `__main__` demo) is documentation. `Embedding` is deliberately *not* re-normalised or otherwise transformed — FaceNet already returns unit-length vectors.

### 2. FaceNet model / library selected

`facenet_pytorch.InceptionResnetV1(pretrained="vggface2", classify=False)`, `.eval()`.

This is FaceNet — the Inception ResNet v1 architecture with the 512-d bottleneck projection that `davidsandberg/facenet` defines. `pretrained="vggface2"` loads weights trained on VGGFace2 (~107 MB, downloaded once on first use, then cached in `~/.cache/torch/checkpoints`). `classify=False` makes the network apply `F.normalize(p=2, dim=1)` internally, i.e. return L2-normalised embeddings — the standard FaceNet behaviour, preserved as the prompt requires. No training, no fine-tuning, no second model, and it is the same library already chosen in Step 1.

### 3. Input / output interface

**Input:** a `uint8` NumPy array of shape `(height, width, 3)` in **BGR** — exactly what `face_detector.detect_faces()` returns in `"face"` and what `cv2.imread` gives for reference photos. One function serves all three sources, which is what makes reference and webcam vectors comparable.

**Output:** `np.ndarray`, shape `(512,)`, dtype `float32`, always L2 norm = 1.0. Because both vectors are unit length, `np.dot(a, b)` *is* the cosine similarity in `[-1, 1]`, so `face_matching.py` needs nothing but a dot product and a threshold.

### 4. Preprocessing (in `_preprocess`, all three steps required by the model)

1. **Colour** — `cvtColor(BGR2RGB)`; the weights expect RGB, OpenCV gives BGR.
2. **Size** — `cv2.resize` to `160x160` (`INTER_AREA`, matching `facenet-pytorch`'s own crop resize). This is the resizing the detector intentionally leaves out.
3. **Normalisation** — `(pixel - 127.5) / 128` mapping `[0,255] → ~[-1,1]`, then HWC→NCHW with a batch dim of 1. Inference runs under `torch.no_grad()`.

### 5–6. Verification results

| Check | Result |
|---|---|
| Model loaded once | first load 0.27 s, next 50 calls **0.006 ms** total, identical object reused |
| CPU support | `cuda.is_available()` False → device `cpu`, params on cpu, full pipeline runs. CUDA auto-used only if present, never required |
| Determinism | two calls byte-identical (`max abs diff = 0.0`) |
| Output | `(512,) float32`, L2 norm `1.000000`, no NaN/Inf |
| Error handling | `None`, `str`, float32, empty, 2-D, 4-channel → all `ValueError` with clear messages. No fake embeddings returned |
| Input compatibility | MTCNN crop, non-square, 27×19, 3000×3000, non-contiguous view → all `(512,) float32`, norm 1.0 |
| Speed (CPU) | 35–66 ms per face; detection+embedding at 640×480 = **76 ms/frame ≈ 13 FPS** |

Semantic check that the embedding actually discriminates identity:

| Pair | Cosine |
|---|---|
| `datatest/test.jpg` vs `lab1/lalala.jpg` (same person, MTCNN crops) | **0.9984** |
| same person, webcam at 640×480 vs 1960×1960 | **0.8784** |
| same person, 320×240 vs 640×480 | **0.9307** |
| `detailed.jpg` faces 1/2/3 vs `test.jpg` (different people) | 0.1145 / 0.0198 / −0.0283 |

Same person lands well above the lecture's 0.7 threshold, different people far below, so the threshold is achievable. One finding worth noting: a loosely hand-cut box around the same face only reached 0.56, which confirms the detector's tight crop matters — MTCNN alignment should be kept in the loop.

I did not touch face matching or webcam integration.

---

## Prompt 4

*2026-09-25 23:03*

**Prompt**

```text
Read:

- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- prompts/03_face_matching.md
- src/face_detector.py
- src/face_embedding.py
- README.md
- docs/plan.md

Then implement exactly the task described in:

prompts/03_face_matching.md

Do not implement webcam integration or main.py yet.

After implementation, show me the changes and test results, then wait for my review.
```

**Response**

All other files read earlier this session and unchanged. Implementing `src/face_matching.py`:

The synthetic-vector helper was wrong (all vectors collapsed to the same direction). Fixing it:

Two fixes needed in the demo: the "empty references" case had its arguments swapped, and I should cover the single-embedding-per-person form.

Now verifying correctness of the un-normalized path, no-NaN guarantee, performance, and end-to-end with real faces:

One real-face "Unknown" case still unverified — using an unregistered face from the same photo:

Implemented `src/face_matching.py`. Only that file changed — `face_detector.py`, `face_embedding.py`, `webcam.py`, `main.py` untouched.

### 1. Changes made

New public interface:

| Symbol | Purpose |
|---|---|
| `calculate_similarity(embedding1, embedding2) -> float` | cosine similarity of two embeddings |
| `match_embedding(query_embedding, reference_embeddings, threshold=0.7) -> dict` | best identity + similarity, or `Unknown` |
| `DEFAULT_THRESHOLD = 0.7` | the one place 0.7 is written |
| `UNKNOWN_LABEL = "Unknown"`, `EMBEDDING_SIZE = 512` | constants used in messages |

The two functions that carry the logic:

```python
def calculate_similarity(embedding1, embedding2) -> float:
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
    # unless the norms say otherwise.
    if math.isclose(norm_product, 1.0, rel_tol=UNIT_NORM_TOLERANCE, abs_tol=0.0):
        return dot_product
    return dot_product / norm_product


def match_embedding(query_embedding, reference_embeddings, threshold=DEFAULT_THRESHOLD):
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
```

Everything else in the file is documentation, input validation, and a deterministic `__main__` demo. The module imports only `math`, `collections.abc` and `numpy` — verified: no `torch`, `cv2` or `facenet_pytorch` in `sys.modules` after importing it.

### 2. Similarity calculation

Cosine similarity measures the angle between two vectors, i.e. "do these point the same way", which for face embeddings means "is this the same person", independent of magnitude. Range `[-1, 1]`. Since FaceNet returns L2-normalised vectors, every embedding has length 1, so `cos(a,b) = (a·b)/(‖a‖‖b‖) = a·b` — the dot product, with no renormalisation. The code still divides by the norm product when it isn't ~1, so it stays mathematically correct for un-normalised input, and it raises `ValueError` on a zero-norm vector rather than emitting NaN.

Verified: un-normalised inputs match the textbook formula to 10 decimals (`-0.0375019307` both ways); identical → `1.0`, opposite → `-1.0`; 300 random pairs all finite and inside `[-1, 1]`.

### 3. Multiple reference images

References are a plain dict — no database, no index:

```python
{"person_01": [emb_01, emb_02, emb_03], "person_02": [emb_01, emb_02]}
```

The query is compared with **every** reference; each person's best similarity is kept; the person with the highest of those wins. Best-per-person rather than averaging, because one photo may be blurred or turned away. A single bare `np.ndarray` per person is also accepted, since one photo per person is the common case. Demo case 4 shows the two-level selection: a query at 30° picks `person_02` (0.9397) over `person_01` (0.8660) because it's closer to that person's 50° photo.

### 4. The 0.7 threshold

`DEFAULT_THRESHOLD = 0.7` is the only literal; `match_embedding` takes it as a parameter, so it can be changed in one place. `similarity >= threshold` → `Matched` with the identity; `< threshold` → `{"label": "Unknown", ...}`. The returned `similarity` is always the value the decision was based on, so the webcam layer can show how close the call was. Validated to be a finite number in `[-1, 1]`. Boundary: case 3 sets the threshold to the exact computed similarity and gets `person_01`; one ULP higher and it flips to `Unknown`.

### 5. Test results

Deterministic synthetic unit vectors — no webcam, no image files, no model download:

```
angle   0 -> +1.0000    angle  60 -> +0.5000
angle  30 -> +0.8660    angle  90 -> +0.0000
angle  45 -> +0.7071    angle 180 -> -1.0000

threshold 0.7:  0/30/45/50 deg -> person_01 (1.0000/0.9397/0.8192/0.7660)
               60/90 deg      -> Unknown   (0.6428/0.1736)
```

All 14 invalid-input cases raise `ValueError` with a specific message: `None`, 2-D, length mismatch (512 vs 256), NaN, Inf, zero norm, empty references dict, references not a dict, empty person list, empty identity name, and thresholds `1.5 / -2.0 / nan / "high"`.

Performance: **42 µs per call** for 2 people / 5 reference embeddings (≈23,600 calls/sec) — negligible against the 76 ms/frame the detector and embedder cost.

End-to-end with real faces (detector → FaceNet → matching, 0.7 threshold):

| Query | Result | Similarity |
|---|---|---|
| registered person, at 1960px | `person_01` | 1.0000 |
| same person at 640×480 (webcam size) | `person_01` | 0.8805 |
| same person at 320×240 (farther) | `person_01` | 0.8253 |
| 2 other registered faces | `person_02` / `person_03` | 1.0000 |
| unregistered face | **`Unknown`** | 0.6518 |

One thing worth flagging: that last row is an unregistered face, but it only scored 0.6518 — just 0.05 below the threshold. Its MTCNN crop was only 19×22 px, and tiny crops give noticeably less discriminative embeddings. So 0.7 works, but the margin is thinner for small/distant faces than for close-up ones. That is a good subject for the threshold survey already listed in `docs/plan.md`.

Not proceeding to webcam integration or `main.py` — waiting for your review.

---

## Prompt 5

*2026-09-25 23:10*

**Prompt**

```text
Read and understand:

- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- prompts/03_face_matching.md
- prompts/04_webcam.md
- src/face_detector.py
- src/face_embedding.py
- src/face_matching.py
- README.md
- docs/plan.md

Then implement exactly the task described in:

prompts/04_webcam.md

Do not integrate face detection, FaceNet, or face matching yet.

After implementation, show me the changes and webcam test results.

Wait for my review before modifying main.py.
```

**Response**

Checking whether a physical webcam is actually reachable from this environment before I claim anything about testing:

A real physical webcam exists here (ACER HD User Facing, UVC). Checking display availability, since `cv2.imshow` needs a GUI:

A real webcam is available (640×480 @ 30fps, and there's a Qt-capable display). Implementing `src/webcam.py`:

Now testing. First the real camera through the module's own functions:

Now the full real loop — real camera, real `imshow` window, with only the keyboard source simulated (no xdotool available to send a real keypress):

Now cleanup-on-exception, camera error handling, and validation:

The validation test was wrong — `@contextmanager` runs its body on `__enter__`, so I must actually use `with`. Re-testing correctly, plus checking a non-zero camera index really works:

Final check — running the module's own `__main__` entry point as a real subprocess and interrupting it:

Both `MTCNN` mentions in `webcam.py` are in docstrings only (lines 25, 33) — no recognition code. Only `webcam.py` changed.

### 1. Changes made

New `src/webcam.py` (243 lines). API:

| Symbol | Purpose |
|---|---|
| `open_webcam(camera_index=0)` | context manager: opens the camera, **always** releases it and destroys windows on exit |
| `read_frame(capture)` | one live BGR frame, or `None` if the frame can't be read |
| `show_frame(frame, window_name=...)` | `cv2.imshow` wrapper, frame shown unmodified |
| `is_exit_key_pressed(exit_key="q")` | `cv2.waitKey` wrapper, `True` only on the exit key |
| `run_webcam_loop(camera_index=0, on_frame=None, exit_key="q", ...)` | the continuous loop; returns the frame count |
| `DEFAULT_CAMERA_INDEX = 0`, `DEFAULT_EXIT_KEY = "q"` | the only place `0` and `"q"` are written |

Imports are only `cv2`, `numpy`, `sys`, `contextlib`, `collections.abc` — no `torch`, no `facenet_pytorch`, no new dependency.

I used a `@contextmanager` rather than a class deliberately: the prompt allows a class only if the resource lifecycle clearly needs one, and `try/finally` in a context manager gives the same guarantee (release + `destroyAllWindows` on normal exit *and* on exceptions) with less code.

### 2. Webcam API

```python
with open_webcam(camera_index=0) as capture:
    frame = read_frame(capture)        # or None
    show_frame(frame)
    if is_exit_key_pressed("q"):
        break
```

`run_webcam_loop` is the loop the final app will use. `on_frame` is the seam for the next step: it receives a frame and returns the frame to display, so `main.py` can later pass a callback that runs MTCNN → FaceNet → matching and draws boxes/labels, **without changing this loop**. With `on_frame=None` it displays raw frames, which is exactly this step's test.

### 3. Frame format

Untouched OpenCV output: `numpy.ndarray`, `uint8`, shape `(height, width, 3)`, BGR. Nothing is resized, converted or encoded. MTCNN's BGR→RGB conversion stays in `face_detector.py` and FaceNet's resize stays in `face_embedding.py`. Verified: 60/60 frames came back `(480, 640, 3)` `uint8`, all identical shape, matching the device's native 640×480.

### 4. Camera cleanup

`open_webcam`'s `finally` block calls `capture.release()` and `cv2.destroyAllWindows()`. Verified all three paths:

- **normal exit** — camera released, `isOpened()` False afterwards
- **exception in the callback** — propagated out, camera immediately re-openable and still delivering frames (no leaked handle)
- **Ctrl+C** — `__main__` subprocess interrupted with SIGINT after 6 s: exit code 0, printed `Webcam 0 opened.` then `Interrupted.`, camera released

### 5. Webcam test results — tested on real hardware

A physical webcam was available (`ACER HD User Facing`, UVC, `/dev/video0`+`/dev/video1`), so this is a genuine test, not a simulated one:

| Test | Result |
|---|---|
| Open + read 60 frames | 60/60, **15.3 FPS** (device reports 30 FPS; UVC delivers ~15 in YUYV here) |
| Frame format | `ndarray`, `uint8`, `(480, 640, 3)` — unmodified |
| Real display window | `imshow` opened and accepted live frames |
| Full loop with camera + window | 30 frames displayed, callback invoked 30×, `q` honoured, released |
| Camera index configurable | `open_webcam(0)` **and** `open_webcam(1)` both open |
| Cannot open (index 7, 99) | `RuntimeError` with clear message, no infinite loop |
| Frame unreadable / device gone | `read_frame` → `None` → loop raises clear `RuntimeError` |
| Exit key | no key → `False`; `q` → `True`; Qt special key `255` → `False` (0xFF mask works) |
| Validation | `-1`, `1.5`, `"0"`, `True` index and `"qq"`/`""`/`5`/`None` exit key → all `ValueError` |

One caveat to be transparent about: **no xdotool/ydotool exists in this environment**, so I could not physically press `q`. The exit-key test replaced only `cv2.waitKey`; the camera, `imshow`, the loop and the cleanup were all genuinely exercised. When you run `python src/webcam.py` yourself, a real `q` press will be handled by the same `is_exit_key_pressed` code path.

Also note OpenCV 5.0.0 printed harmless Qt warnings (`Could not find the Qt platform plugin "wayland"`, missing font dir). The window still opened via the X11 fallback on `DISPLAY=:1`. That's a packaging quirk of the `opencv-python` wheel, not a code issue — but you may see those lines on your machine too.

Not touching `main.py` — waiting for your review.

---

## Prompt 6

*2026-09-25 23:14*

**Prompt**

```text
Read and understand:

- prompts/00_project_architecture.md
- prompts/01_face_detection.md
- prompts/02_face_embedding.md
- prompts/03_face_matching.md
- prompts/04_webcam.md
- prompts/05_main_integration.md
- src/face_detector.py
- src/face_embedding.py
- src/face_matching.py
- src/webcam.py
- README.md
- docs/plan.md

Then implement exactly the task described in:

prompts/05_main_integration.md

This is the final integration step.

Do not redesign or rewrite the existing modules unless a real integration bug requires a minimal change.

Use the existing module interfaces.

After implementation, run the complete application with the physical webcam if available and report the actual test results.

Do not add functionality beyond the practical assignment.
```

**Response**

Prompt 05 is already stored at `prompts/05_main_integration.md` (that's the file I just read). One design question needs data first: prompt 05 Step 1 says to feed reference images straight to FaceNet, but FaceNet expects *face crops* (prompt 01's pipeline is explicit about that). Let me measure the difference:

Decisive: an uncropped reference photo scores **0.07** against a webcam crop — below the 0.7 threshold, so recognition would fail completely. Reference images must be cropped with the existing `detect_faces` before embedding. Writing `main.py`:

Error paths are clean. Now Test A (reference loading) — building a temp dataset from face photos that already exist in the repo:

Test A passes. Now checking what the physical webcam actually sees before running the app:

A real face is in front of the camera (30/30 frames). Running the **actual application** against the physical webcam now:

Now capturing what the live loop actually computes and draws, using the same `process_frame` on genuine webcam frames:

I can't view images directly, so let me verify the drawing programmatically instead:

The remaining Test C items (a *known* person recognized) can't come from the live camera — the person in front of it isn't in the repo's reference photos. Verifying that path through the identical `process_frame` with real photos:

My test picked the wrong "stranger" — `det[2]` is exactly the face that got registered as person_02 (highest confidence, 0.842). Re-running with a genuinely unregistered face:

> **Note:** opencode auto-generated a context-compaction summary at this point
> (an internal snapshot of the work state, not a reply to the prompt). It is
> omitted here; see the raw session for its full contents.

---

## Prompt 7

*2026-09-25 23:19*

**Prompt**

Continue if you have next steps, or stop and ask for clarification if you are unsure how to proceed.

**Response**

All verification passed. Now the documentation and cleanup that remain. Let me re-read the final prompt's documentation requirements plus the two files to update.

Now let me confirm the exact threshold operator and CLI help text so the docs are accurate:

Now the targeted README updates (keeping it concise, not a rewrite):

Now marking the plan's implementation steps complete:

Cleaning caches and doing a final end-to-end run of the real application with FPS measurement:

6.4 FPS is an artifact of my harness (I called `detect_faces` a second time per frame). Measuring the app loop exactly as `main.py` runs it:

Counter bug in my measurement script (I dropped `frames += 1`). Re-running:

Adding the measured real-time performance to the plan:

Now the final project tree and a check that no stray files were left behind:

Everything is implemented, verified on the physical webcam, and documented.

## What was built

`main.py` wires the four existing modules into one real-time loop and adds nothing beyond the assignment:

```
data/faces/  ->  MTCNN + FaceNet  ->  reference embeddings   (once, at start)
webcam       ->  MTCNN            ->  face crops             (every frame)
             ->  FaceNet          ->  live embeddings        (every frame)
             ->  cosine similarity->  threshold 0.7          (every frame)
             ->  draw + display   ->  the labelled frame     (every frame)
```

CLI: `--camera N` (default 0), `--threshold F` (default 0.7), `--data-dir PATH` (default `data/faces`).

One design decision worth flagging: reference photos are passed through the same `detect_faces()` before FaceNet. Feeding a whole photo to FaceNet instead of a face crop gives `0.0725` similarity for the same person that scores `0.9984` when cropped — recognition simply fails. Using the existing detector keeps the reference and live paths identical.

## Real webcam results (ACER HD User Facing UVC, 640×480)

| Check | Result |
|---|---|
| Reference loading | Once at start, reused for all 197 frames |
| Face detection | 24 real frames → 26 faces (20×1 face, 3×2 faces, 1×0 faces) |
| Threshold 0.7 | All 26 live faces `Unknown`, similarities 0.1442–0.6317 (max < 0.7) |
| Drawing verified | All 4 box edges + label drawn, 2497 red px, 0 green |
| Known person | `test.jpg` → `person_01 1.00`, 8173 green px, 0 red |
| Multi-face frame | 3 faces all processed independently, not just the first |
| No-face frame | Returned untouched, loop continues |
| Performance | 13.8 FPS raw capture → 9.8 FPS full pipeline (CPU-only) |
| Exit | `q` handled; camera released cleanly; SIGINT exits 0 |

## Honest limitation

A live *matched* result could not be shown, because the person in front of the camera is not in the repository's reference photos. The project architecture forbids writing webcam frames into `data/faces/`, so I did not create a reference from the live image. To see a green match on camera, add your own photo to `data/faces/person_01/`. The matched path is verified through the identical `process_frame()` using real photos.

Two caveats on the numbers: the earlier 6.4 FPS reading was my measurement harness calling `detect_faces` twice per frame, not the application. Also, automated `q` injection was impossible (`xdotool` absent), so real-camera runs were stopped with SIGINT; the `q` branch was tested separately by substituting only `cv2.waitKey`.

## Files

Modified: `main.py` (new integration), `README.md` (run instructions with the Python 3.14 `--no-deps` note), `docs/plan.md` (steps marked complete + measured results). No existing module needed changes — their interfaces worked as specified. `__pycache__` cleaned; `data/faces/` still holds only its two `.gitkeep` files.
---
