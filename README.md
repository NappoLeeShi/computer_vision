# Computer Vision — Lab Assignments

Five practical assignments for a Computer Vision course, built in Python with
OpenCV, Pillow, Matplotlib, NumPy, Scikit-image, PyWavelets, MTCNN and FaceNet.
Each lab lives in its own folder and is self-contained.

## Project architecture

```
computer_vision/
├── datatest/            # shared test images used across labs
├── lab1/                # basic OpenCV / Pillow operations
│   ├── docs/            # plan.md, implementation.md
│   ├── outputs/         # saved result images
│   ├── main.ipynb
│   └── main.py
├── lab2/                # point operators, linear & non-linear filters
│   ├── docs/            # plan.md, implementation.md, evidence.md
│   ├── main.ipynb
│   └── prompt_lab2_part2.txt
├── lab3/                # Canny edge detection
│   ├── docs/            # plan.md, implementation.md, evidence.md
│   └── main.ipynb
├── lab4/                # wavelet-hash image similarity
│   ├── agent_sessions/  # recorded agent session + extracted prompts
│   ├── prompts/         # prompt files 00–05
│   ├── data/            # generated similar / dissimilar image pairs
│   ├── original_images/ # source images for dataset generation
│   ├── results/         # metrics and plots
│   ├── src/             # wavelet_hash, matching, evaluation, dataset_generator
│   ├── docs/plan.md
│   ├── main.ipynb
│   └── README.md
├── lab5/                # real-time face recognition (FaceNet + MTCNN)
│   ├── agent_sessions/  # recorded agent session + extracted prompts
│   ├── prompts/         # prompt files 00–05
│   ├── data/faces/      # reference images, one folder per person
│   ├── results/         # reference embeddings
│   ├── src/             # face_detector, face_embedding, face_matching, webcam
│   ├── docs/plan.md
│   ├── main.py
│   └── README.md
├── prompts_and_sessions/ # collected prompts & sessions for all labs
│   ├── lab1/
│   ├── lab2/
│   ├── lab3/
│   ├── lab4/            # agent_sessions/ + prompts/ copied from lab4
│   └── lab5/            # agent_sessions/ + prompts/ copied from lab5
└── .venv/               # shared virtual environment
```

## The labs

| Lab | Topic | Summary | Entry point |
| --- | --- | --- | --- |
| 1 | OpenCV / Pillow basics | Read, display and save images; convert colour spaces (grayscale, HSV, LAB); crop and resize; draw shapes and text. | `lab1/main.ipynb`, `lab1/main.py` |
| 2 | Image operators & filters | Brightness, contrast, negative image and thresholding; mean, Gaussian and sharpening filters; advanced work on Sobel/Prewitt edge detection, custom kernels, filter comparison, and non-linear median/bilateral filters. | `lab2/main.ipynb` |
| 3 | Canny edge detection | Canny with OpenCV and Scikit-image; parameter sweeps (sigma, low/high thresholds); Canny on noisy, low-contrast and fine-detail images; combining Canny with contour and Hough shape detection. | `lab3/main.ipynb` |
| 4 | Wavelet-hash image similarity | Build similar/dissimilar image pairs, apply a wavelet transform, quantise coefficients into a hash, compare hashes with Hamming distance, and evaluate with accuracy, sensitivity, specificity and a ROC curve. | `lab4/main.ipynb` |
| 5 | Real-time face recognition | Capture webcam frames with OpenCV, detect faces with MTCNN, extract FaceNet embeddings, compare them against reference embeddings and apply a similarity threshold to print "Matched" or "Unknown" on the live frame. | `lab5/main.py` |

## Where to find the prompts

Every prompt used to build a lab is kept in that lab's own folder, and a copy of
all of them is collected in `prompts_and_sessions/`.

**Lab 1** — `lab1/docs/`
- `prompts_and_sessions/lab1/plan.md` — objectives, requirements and task breakdown
- `prompts_and_sessions/lab1/implementation.md` — directory tree and walkthrough

**Lab 2** — `lab2/docs/` and `lab2/prompt_lab2_part2.txt`
- `prompts_and_sessions/lab2/plan.md` — task requirements and member assignment
- `prompts_and_sessions/lab2/evidence.md` — the "Prompt 1 / Prompt 2" edge-detection prompts and results
- `prompts_and_sessions/lab2/prompt_lab2_part2.txt` — raw prompt for part 2
- `prompts_and_sessions/lab2/implementation.md` — directory tree and walkthrough

**Lab 3** — `lab3/docs/`
- `prompts_and_sessions/lab3/evidence.md` — the Canny parameter-sweep and shape-detection prompts
- `prompts_and_sessions/lab3/plan.md` — task requirements and member assignment
- `prompts_and_sessions/lab3/implementation.md` — directory tree and walkthrough

**Lab 4** — `lab4/prompts/` and `lab4/agent_sessions/`
- `lab4/prompts/00_project_architecture.md` … `05_full_pipeline_implementation.md` — the ordered prompt files
- `lab4/agent_sessions/lab4_prompting.md` — every prompt with the assistant responses, in order
- `lab4/agent_sessions/lab4_session.json` — the raw exported session
- `prompts_and_sessions/lab4/prompts/` and `prompts_and_sessions/lab4/agent_sessions/` — copies

**Lab 5** — `lab5/prompts/` and `lab5/agent_sessions/`
- `lab5/prompts/00_project_architecture.md` … `05_main_integration.md` — the ordered prompt files
- `lab5/agent_sessions/lab5_prompting.md` — every prompt with the assistant responses, in order
- `lab5/agent_sessions/lab5_session.json` — the raw exported session
- `prompts_and_sessions/lab5/prompts/` and `prompts_and_sessions/lab5/agent_sessions/` — copies

## Opening a session JSON file
To load the session back into opencode and continue or browse it in the TUI:

```bash
opencode import lab5/agent_sessions/lab5_session.json
opencode
```

If you only want to read the conversation, prefer the pre-extracted
`lab5/agent_sessions/lab5_prompting.md`, which renders each prompt together with
its responses as plain Markdown.
