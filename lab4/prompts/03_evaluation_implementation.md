Now implement Step 4 of the project.

Focus ONLY on:

src/evaluation.py

The purpose of this module is to evaluate the Wavelet Hash image matching method.

The lecture requires evaluation using:

- Accuracy
- Sensitivity
- Specificity
- ROC curve

Use the results produced by src/matching.py.

Do NOT implement a machine learning classifier.

Requirements:

1. Implement functions to calculate:

- True Positive (TP)
- True Negative (TN)
- False Positive (FP)
- False Negative (FN)

based on:
- ground_truth
- predicted_label

Use:
1 = similar
0 = dissimilar

2. Implement:

calculate_accuracy(...)

Accuracy:

(TP + TN) / (TP + TN + FP + FN)

3. Implement:

calculate_sensitivity(...)

Sensitivity:

TP / (TP + FN)

4. Implement:

calculate_specificity(...)

Specificity:

TN / (TN + FP)

Handle division-by-zero cases safely.

5. Implement a function that evaluates a list of matching results returned by:

compare_image_pairs()

The function should return a simple dictionary containing:

- TP
- TN
- FP
- FN
- accuracy
- sensitivity
- specificity

6. Implement ROC evaluation.

The matching method uses Hamming distance, where:

smaller distance = more similar
larger distance = more dissimilar

Therefore, generate predictions using multiple Hamming-distance thresholds.

For each threshold:

distance <= threshold
    → similar

distance > threshold
    → dissimilar

For each threshold calculate:

True Positive Rate (TPR)
False Positive Rate (FPR)

where:

TPR = Sensitivity = TP / (TP + FN)

FPR = FP / (FP + TN)

Return the threshold values, FPR values, and TPR values in a simple structure that can be used to plot an ROC curve.

7. Add a simple function to plot the ROC curve.

Save the plot to:

results/plots/roc_curve.png

Create the results/plots directory if it does not exist.

8. Save evaluation metrics to:

results/metrics/

Use a simple format such as JSON.

Do not create a database or complicated reporting system.

9. Do not require the dataset to exist yet.

The functions should accept data/results as arguments rather than hard-coding image filenames.

10. Keep the implementation simple and suitable for a university Computer Vision practical assignment.

Do NOT:
- use machine learning
- train a model
- use deep learning
- use SIFT
- use SURF
- use ORB
- add unnecessary classes
- add unnecessary abstractions
- add unnecessary dependencies

11. Reuse the logic from matching.py where appropriate instead of duplicating Wavelet Hash code.

12. Do not modify wavelet_hash.py or matching.py unless absolutely necessary.

13. Add a small ```__main__``` section that only demonstrates usage or prints a usage message. It must not assume that the dataset exists.

14. After implementation, explain briefly:
- how Accuracy is calculated
- how Sensitivity is calculated
- how Specificity is calculated
- how changing the Hamming threshold produces the ROC curve

Do not proceed to dataset preparation or README modifications yet.