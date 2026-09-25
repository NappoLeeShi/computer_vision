Now implement Step 2 of the project.

Focus ONLY on:

src/wavelet_hash.py

Do not implement image matching, evaluation, ROC, or dataset processing yet.

The goal of this module is to implement the basic Wavelet Hash pipeline described in the lecture:

Image
→ preprocessing
→ wavelet transform
→ coefficient quantization
→ binary hash

The module should also provide Hamming distance calculation between two hashes.

Requirements:

1. Use Python and PyWavelets (pywt) for the wavelet transform.

2. Implement a simple grayscale image preprocessing step:
   - Load an image from a file path.
   - Convert it to grayscale.
   - Resize it to a consistent small size before applying the wavelet transform.

3. Implement a wavelet transform function.

4. Implement coefficient quantization:
   - Convert the selected wavelet coefficients into a binary representation.
   - Keep the method simple and easy to explain in a university Computer Vision assignment.

5. Implement a function that generates a wavelet hash from an image.

6. Implement a Hamming distance function that compares two binary hashes.

7. Keep the implementation simple.
   Do NOT:
   - use machine learning
   - use deep learning
   - use SIFT
   - use SURF
   - use ORB
   - use neural networks
   - add unnecessary classes or abstractions
   - add unnecessary dependencies

8. Use clear function names and short docstrings.

9. Make sure the functions can later be imported by:
   - src/matching.py
   - main.ipynb

10. The implementation should not depend on the dataset being present yet.

11. Add a small executable test section under:
```python
if __name__ == "__main__":
```
This test should:
   - explain that a real image path is required
   - NOT assume that a dataset already exists
   - avoid crashing when no test image is available.

12. Update requirements.txt only if a new dependency is actually required.

13. Do not modify matching.py or evaluation.py yet.

14. Do not modify the overall project structure.

After implementation:
- Show the contents/summary of src/wavelet_hash.py.
- Explain briefly how the implementation follows:
  Wavelet Transform → Quantization → Hash → Hamming Distance.
- Do not proceed to the next step.

You must use the virtual environment `.venv` to install libraries. This folder is located in `lab4/../.venv/` (The root folder, which also contains the `lab4` folder.)