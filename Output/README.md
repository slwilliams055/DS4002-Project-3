# ResNet50 Deepfake Detection — Output

This folder contains the supplied model results in the same style as the referenced repository’s `Output` directory.

- `model_results_summary.txt`: dataset, model, results, baseline, and limitations
- `classification_metrics.csv`: overall evaluation metrics
- `confusion_matrix.csv`: observed REAL/FAKE classification counts
- `training_history.csv`: training and validation results for all 20 epochs
- `training_validation_accuracy.png`: accuracy curves from epoch logs
- `training_validation_loss.png`: loss curves from epoch logs
- `model_accuracy_comparison.png`: baseline, validation, training, and test accuracies

**Caution:** Validation accuracy of 50.83% is much lower than test accuracy of 97.81%. This discrepancy must be investigated. No model was rerun; all charts are based on the provided output.
