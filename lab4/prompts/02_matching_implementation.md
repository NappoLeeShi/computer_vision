Now implement Step 3 of the project.

Focus ONLY on:

src/matching.py

Do not implement the evaluation metrics or ROC curve yet.
Do not modify evaluation.py.
Do not require a real dataset yet.

The purpose of this module is to compare two images using the Wavelet Hash implementation from:

src/wavelet_hash.py

The intended pipeline is:

Image A
    ↓
Wavelet Hash
    ↓
Hash A
             → Hamming Distance → Similar / Dissimilar
    ↑
Wavelet Hash
    ↑
Image B

Requirements:

1. Import and reuse the functions already implemented in:

src/wavelet_hash.py

In particular, reuse:
- generate_wavelet_hash()
- hamming_distance()

Do NOT duplicate the Wavelet Hash implementation inside matching.py.

2. Implement a function similar to:

compare_images(image1_path, image2_path, threshold=...)

It should:

- Generate a Wavelet Hash for image 1.
- Generate a Wavelet Hash for image 2.
- Calculate the Hamming distance.
- Compare the distance with a configurable threshold.
- Return the comparison result.

The result should contain enough information for later evaluation, including:
- image 1 path
- image 2 path
- Hamming distance
- threshold
- predicted label

Use:

predicted label = 1  → similar
predicted label = 0  → dissimilar

The decision rule should be:

distance <= threshold
    → predicted similar (1)

distance > threshold
    → predicted dissimilar (0)

3. Do NOT choose a threshold based on a real dataset yet.

Use a simple default threshold only so the function can be tested.

Make the threshold configurable.

4. Add a function for comparing multiple image pairs if this can be done simply.

For example:

compare_image_pairs(pairs, threshold=...)

where each pair contains:
- image1 path
- image2 path
- ground-truth label

The function should return simple structured results that can later be passed to evaluation.py.

Do not build a complicated dataset framework.

5. The module should work even though the data/ directory is currently empty.

Do not hard-code filenames or assume that specific images exist.

6. Add a small test/demo section under:
```python
if __name__ == "__main__":
```
It should not require real dataset images.

If no image paths are provided, simply print a short usage example instead of crashing.

7. Keep the implementation simple and suitable for a university Computer Vision practical assignment.

Do NOT:
- use machine learning
- use deep learning
- use SIFT
- use SURF
- use ORB
- use a classifier
- create unnecessary classes
- create a database
- create a web interface
- add unnecessary dependencies
- implement ROC or evaluation metrics yet

8. Do not modify the existing wavelet_hash.py implementation unless absolutely necessary.
If you believe a change is necessary, explain why instead of silently changing it.

9. Keep the code easy to understand because this code will later be explained in the practical report.

10. After implementation:
- Show the resulting matching.py structure or summarize its functions.
- Explain briefly how it uses Wavelet Hash and Hamming distance.
- Do not proceed to evaluation.py yet.