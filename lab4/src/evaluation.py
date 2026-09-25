"""Evaluate Wavelet Hash matching results and plot an ROC curve."""

import json
from collections.abc import Mapping, Sequence
from pathlib import Path


DEFAULT_METRICS_PATH = Path("results/metrics/evaluation_metrics.json")
DEFAULT_PLOT_PATH = Path("results/plots/roc_curve.png")


def _validate_label(value: object, field_name: str) -> int:
    if value not in (0, 1):
        raise ValueError(f"{field_name} must be 0 or 1.")
    return int(value)


def _confusion_counts(
    ground_truth: Sequence[int],
    predicted_labels: Sequence[int],
) -> dict[str, int]:
    if len(ground_truth) != len(predicted_labels):
        raise ValueError("Ground truth and predictions must have equal lengths.")

    counts = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
    for truth, prediction in zip(ground_truth, predicted_labels):
        if truth == 1 and prediction == 1:
            counts["TP"] += 1
        elif truth == 0 and prediction == 0:
            counts["TN"] += 1
        elif truth == 0 and prediction == 1:
            counts["FP"] += 1
        else:
            counts["FN"] += 1
    return counts


def calculate_confusion_counts(
    results: Sequence[Mapping[str, object]],
) -> dict[str, int]:
    """Calculate TP, TN, FP, and FN from compare_image_pairs() results."""
    ground_truth = []
    predicted_labels = []
    for result in results:
        if not isinstance(result, Mapping):
            raise ValueError("Each matching result must be a mapping.")
        try:
            truth = _validate_label(result["ground_truth"], "ground_truth")
            prediction = _validate_label(
                result["predicted_label"], "predicted_label"
            )
        except KeyError as error:
            raise ValueError("Matching results must contain labels.") from error
        ground_truth.append(truth)
        predicted_labels.append(prediction)

    return _confusion_counts(ground_truth, predicted_labels)


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def calculate_accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
    """Calculate accuracy as (TP + TN) / (TP + TN + FP + FN)."""
    return _safe_ratio(tp + tn, tp + tn + fp + fn)


def calculate_sensitivity(tp: int, fn: int) -> float:
    """Calculate sensitivity as TP / (TP + FN)."""
    return _safe_ratio(tp, tp + fn)


def calculate_specificity(tn: int, fp: int) -> float:
    """Calculate specificity as TN / (TN + FP)."""
    return _safe_ratio(tn, tn + fp)


def evaluate_matching_results(
    results: Sequence[Mapping[str, object]],
) -> dict[str, int | float]:
    """Evaluate matching results and return counts plus three metrics."""
    counts = calculate_confusion_counts(results)
    return {
        **counts,
        "accuracy": calculate_accuracy(
            counts["TP"], counts["TN"], counts["FP"], counts["FN"]
        ),
        "sensitivity": calculate_sensitivity(counts["TP"], counts["FN"]),
        "specificity": calculate_specificity(counts["TN"], counts["FP"]),
    }


def calculate_roc_curve(
    results: Sequence[Mapping[str, object]],
    thresholds: Sequence[int] | None = None,
) -> dict[str, list[int] | list[float]]:
    """Calculate ROC points over multiple Hamming-distance thresholds."""
    ground_truth = []
    distances = []
    for result in results:
        if not isinstance(result, Mapping):
            raise ValueError("Each matching result must be a mapping.")
        try:
            truth = _validate_label(result["ground_truth"], "ground_truth")
            distance = result["hamming_distance"]
        except KeyError as error:
            raise ValueError(
                "Matching results must contain labels and distances."
            ) from error
        if not isinstance(distance, int) or distance < 0:
            raise ValueError("Hamming distances must be non-negative integers.")
        ground_truth.append(truth)
        distances.append(distance)

    if thresholds is None:
        selected_thresholds = list(range(max(distances, default=0) + 2))
    else:
        selected_thresholds = [int(threshold) for threshold in thresholds]
        if any(threshold < 0 for threshold in selected_thresholds):
            raise ValueError("ROC thresholds must be non-negative integers.")

    fpr_values = []
    tpr_values = []
    for threshold in selected_thresholds:
        predicted_labels = [int(distance <= threshold) for distance in distances]
        counts = _confusion_counts(ground_truth, predicted_labels)
        fpr_values.append(
            _safe_ratio(counts["FP"], counts["FP"] + counts["TN"])
        )
        tpr_values.append(
            _safe_ratio(counts["TP"], counts["TP"] + counts["FN"])
        )

    return {
        "thresholds": selected_thresholds,
        "fpr": fpr_values,
        "tpr": tpr_values,
    }


def plot_roc_curve(
    roc_data: Mapping[str, Sequence[float]],
    output_path: str | Path = DEFAULT_PLOT_PATH,
) -> Path:
    """Plot an ROC curve and save it as a PNG image."""
    import matplotlib.pyplot as plt

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots()
    axis.plot(roc_data["fpr"], roc_data["tpr"], label="Wavelet Hash")
    axis.plot([0.0, 1.0], [0.0, 1.0], "--", label="Random")
    axis.set_xlabel("False Positive Rate")
    axis.set_ylabel("True Positive Rate")
    axis.set_title("ROC Curve")
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output, format="png")
    plt.close(figure)
    return output


def save_evaluation_metrics(
    metrics: Mapping[str, object],
    output_path: str | Path = DEFAULT_METRICS_PATH,
) -> Path:
    """Save evaluation metrics as a simple JSON file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=2, sort_keys=True)
    return output


if __name__ == "__main__":
    print("Usage: call evaluate_matching_results(results) with matching results.")
    print("Use calculate_roc_curve(results) and plot_roc_curve() for ROC output.")
