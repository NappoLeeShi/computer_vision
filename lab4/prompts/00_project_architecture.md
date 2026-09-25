We are going to implement a simple Computer Vision practical assignment based strictly on the provided lecture material.

The assignment is:

"Comparing Image Similarity Using Wavelet Hash in Python"

The required pipeline from the lecture is:

1. Prepare a dataset containing similar image pairs and dissimilar image pairs.
2. Apply a wavelet transform to each image.
3. Quantize the wavelet coefficients.
4. Generate a hash for each image based on the quantized wavelet coefficients.
5. Calculate the Hamming distance between image hashes.
6. Use the distance to determine whether two images are similar or dissimilar.
7. Evaluate the method using:
   - Accuracy
   - Sensitivity
   - Specificity
   - ROC curve

For now, DO NOT implement the algorithm.

Your task in this step is only to create the initial project structure.

Create the following structure:

```
wavelet_image_matching/ (lab4)
├── README.md
│
├── prompts/
│   └── 00_project_architecture.md
│
├── data/
│   ├── similar/
│   └── dissimilar/
│
├── src/
│   ├── wavelet_hash.py
│   ├── matching.py
│   └── evaluation.py
│
└── results/
    ├── hashes/
    ├── metrics/
    └── plots/
```
Do NOT create a new folder called `wavelet_image_matching`. This folder should be the current working directory: `lab4`. Do not go out of this working directory unless prompted.

Requirements:
- Create all directories and files.
- README.md should briefly explain:
  - the purpose of the project
  - the overall image similarity pipeline
  - what each directory/file is responsible for
- The source files should contain only short comments/docstrings explaining their future responsibility. Do not implement the actual algorithms yet.
- prompts/00_project_architecture.md should contain this exact instruction/prompt that is being used for this step.
- Keep the project simple and suitable for a university Computer Vision practical assignment.
- Do not add unnecessary frameworks, classes, abstractions, configuration systems, tests, notebooks, databases, web applications, machine learning models, or deep learning models.
- Do not implement SIFT, SURF, ORB, or other feature-matching algorithms.
- Do not implement the advanced tasks from the lecture yet.
- Do not invent a dataset yet.

After creating the structure, show me the resulting directory tree and briefly explain what was created.

Do not proceed to implementing the Wavelet Hash algorithm until I give the next instruction.