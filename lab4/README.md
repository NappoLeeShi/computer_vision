# Wavelet Image Matching

This project is a simple Computer Vision practical assignment for comparing image similarity using wavelet hashes.

## Purpose

The project will prepare similar and dissimilar image pairs, apply a wavelet transform to each image, quantize the resulting coefficients, and generate a hash for each image. Hamming distances between hashes will then be used to classify image pairs and evaluate the method using accuracy, sensitivity, specificity, and a ROC curve.

This initial version contains only the project structure. The image-matching algorithm is not implemented yet.

## Project structure

- `README.md`: project overview and structure.
- `prompts/00_project_architecture.md`: instructions for the initial project setup.
- `data/similar/`: image pairs that should be classified as similar.
- `data/dissimilar/`: image pairs that should be classified as dissimilar.
- `src/wavelet_hash.py`: future wavelet transformation, coefficient quantization, and hash generation.
- `src/matching.py`: future Hamming-distance comparison and similarity classification.
- `src/evaluation.py`: future metric calculation and ROC-curve evaluation.
- `results/hashes/`: generated image hashes.
- `results/metrics/`: calculated evaluation metrics.
- `results/plots/`: generated evaluation plots, including the ROC curve.

## Dataset generation

- `original_images/` contains source images.
- `src/dataset_generator.py` generates similar and dissimilar image pairs.
- Generated pairs are stored under `data/`.

## Running the project

1. Put source images in `original_images/` and generate pairs, or place existing pairs under `data/`.
2. Open `main.ipynb`.
3. Run the notebook from top to bottom from the project root.
4. Check `results/` for the saved metrics and the ROC plot.
