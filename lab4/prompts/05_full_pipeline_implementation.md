Now integrate the existing project modules into one complete end-to-end workflow using:

main.ipynb

Do NOT include src/dataset_generator.py in the workflow.

The existing core modules are:

src/
├── wavelet_hash.py
├── matching.py
└── evaluation.py

The purpose of main.ipynb is to demonstrate the complete Wavelet Hash image matching practical assignment from input data to final evaluation.

## Overall pipeline

The notebook should implement this flow:

Dataset
↓
Load similar and dissimilar image pairs
↓
Generate Wavelet Hashes
↓
Calculate Hamming Distance
↓
Predict Similar / Dissimilar
↓
Compare with Ground Truth
↓
TP / TN / FP / FN
↓
Accuracy
Sensitivity
Specificity
↓
Evaluate multiple Hamming thresholds
↓
ROC Curve
↓
Save results

## Important

Reuse the existing implementations.

Do NOT rewrite the algorithms inside main.ipynb.

Use the functions already implemented in:

src/wavelet_hash.py

* generate_wavelet_hash()
* hamming_distance()

src/matching.py

* compare_images()
* compare_image_pairs()

src/evaluation.py

* calculate_confusion_counts()
* calculate_accuracy()
* calculate_sensitivity()
* calculate_specificity()
* evaluate_matching_results()
* calculate_roc_curve()
* plot_roc_curve()
* save_evaluation_metrics()

Do not duplicate their implementations in the notebook.

## Notebook structure

Organize main.ipynb into clear sections using Markdown cells.

### 1. Title and Introduction

Briefly explain:

* This notebook implements the Wavelet Hash image similarity practical.
* The goal is to compare similar and dissimilar image pairs.
* The method uses Wavelet Transform, quantization, hashing, and Hamming distance.

Keep this short.

### 2. Imports

Import the required Python libraries and the existing project modules.

Make sure imports work when running:

jupyter notebook main.ipynb

from the project root.

If necessary, use a simple and clear Python path setup.

Do NOT introduce a package manager or complicated project configuration.

### 3. Configuration

Create a small configuration section containing:

* data directory
* similar pairs directory
* dissimilar pairs directory
* Hamming distance threshold

For example:

DATA_DIR = Path("data")
SIMILAR_DIR = DATA_DIR / "similar"
DISSIMILAR_DIR = DATA_DIR / "dissimilar"

Keep these values easy to change.

Do not hard-code individual image filenames.

### 4. Discover Dataset Pairs

Automatically discover pair directories inside:

data/similar/
data/dissimilar/

Each pair directory contains:

image1.jpg
image2.jpg

Create a list of pairs in the format expected by:

compare_image_pairs()

Assign:

similar = 1
dissimilar = 0

Do not depend on a fixed number of pairs.

If the dataset is empty, display a clear message explaining that images must be placed in the data directories.

Do not crash because the dataset is empty.

### 5. Run Image Matching

Use:

compare_image_pairs()

to process all discovered pairs.

Display a compact table containing information such as:

* pair type / ground truth
* image names
* Hamming distance
* predicted label

Do not display excessively large output.

### 6. Evaluate the Selected Threshold

Use:

evaluate_matching_results()

to calculate:

* TP
* TN
* FP
* FN
* Accuracy
* Sensitivity
* Specificity

Display the results clearly.

For example:

## Metric              Value

Accuracy            ...
Sensitivity         ...
Specificity         ...
TP                  ...
TN                  ...
FP                  ...
FN                  ...

Do not manually recalculate these metrics in the notebook.

Use the functions from evaluation.py.

### 7. ROC Curve

Use:

calculate_roc_curve()

to evaluate multiple Hamming-distance thresholds.

Then use:

plot_roc_curve()

to generate and save:

results/plots/roc_curve.png

Display the ROC curve in the notebook.

Explain briefly that:

* each threshold produces a different similarity decision
* TPR = Sensitivity
* FPR = FP / (FP + TN)
* changing the threshold produces the ROC curve

Do not implement another ROC algorithm in the notebook.

### 8. Save Evaluation Results

Use:

save_evaluation_metrics()

to save the selected-threshold evaluation results to:

results/metrics/evaluation_metrics.json

Make sure:

results/metrics/
results/plots/

are created automatically if necessary.

### 9. Final Summary

Add a short Markdown section summarizing:

* number of similar pairs
* number of dissimilar pairs
* selected Hamming threshold
* Accuracy
* Sensitivity
* Specificity
* location of the ROC plot
* location of the JSON metrics file

Do not add unnecessary analysis.

## Error handling

The notebook should handle:

* empty dataset directories
* missing pair directories
* pair directories without exactly two image files
* unsupported image formats

Do not silently ignore problems.

Use simple messages explaining what needs to be fixed.

## Important constraints

Keep the notebook simple and suitable for a university Computer Vision practical.

Do NOT:

* implement machine learning
* implement deep learning
* use SIFT
* use SURF
* use ORB
* add a classifier
* add a GUI
* add a web application
* add unnecessary abstractions
* duplicate algorithms already implemented in src/
* call dataset_generator.py
* create additional source modules unless absolutely necessary

The notebook is an integration/demo layer, not another implementation of the algorithms.

## Prompt logging

Create:

prompts/03_project_integration.md

and store this complete prompt inside it.

Do not modify previous prompt files.

## README

Only make a minimal update to README.md if necessary.

Add a short "Running the project" section explaining:

1. Put source/generated image pairs under data/.
2. Open main.ipynb.
3. Run the notebook from top to bottom.
4. Check results/ for metrics and ROC output.

Do not rewrite the existing README unnecessarily.

## Final check

After creating main.ipynb:

1. Verify that the notebook can run from the project root.
2. Verify that imports reference the existing modules.
3. Verify that no dataset_generator.py code is used.
4. Verify that matching.py is responsible for matching.
5. Verify that evaluation.py is responsible for evaluation.
6. Verify that the notebook only orchestrates the existing modules.

If the dataset is currently empty, do not invent test images and do not fail the entire project because of the missing dataset.

Instead, make the notebook ready to run once data is added.

At the end, show the final project tree and briefly explain the complete execution flow.

Do not add new functionality beyond this integration task.
