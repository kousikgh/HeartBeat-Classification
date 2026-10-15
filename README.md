# AI-Based Heartbeat Classification System Using Machine Learning

An academic/research prototype for ECG heartbeat classification. It is not a
medical device and must not be used for diagnosis or clinical decision-making.

## Phase 1 status

The initial Flask application scaffold and project folders are ready. Dataset
preparation, feature extraction, training, and prediction will be implemented
in later phases after the MIT-BIH dataset is inspected.

## Dataset setup

The MIT-BIH dataset is not included and will never be downloaded automatically
by this project. Follow [docs/dataset_setup.md](docs/dataset_setup.md) to
download it manually from PhysioNet and inspect the local copy read-only.

## Preprocessing approach

The pipeline validates a single finite ECG signal, applies a zero-phase 0.5–40
Hz fourth-order Butterworth band-pass filter, and z-score normalizes the result.
This reduces baseline wander and higher-frequency noise while preserving timing
for later heartbeat segmentation. Training and the future Flask interface will
use the same pipeline to avoid inconsistent processing.

## Heartbeat representation and labels

Each supported reference annotation becomes a fixed 0.65-second window (0.25 s
before and 0.40 s after the annotated R peak). The centrally defined mapping in
`src/labels.py` maps supported MIT-BIH symbols to NORMAL, SUPRAVENTRICULAR,
VENTRICULAR, FUSION, or UNKNOWN. Rhythm markers and unsupported symbols are
excluded. Features deliberately avoid heuristic QRS-duration estimates; they
include time-domain values, R-peak context, prior RR timing, and FFT summaries.

## Training design

`scripts/prepare_data.py` converts each locally stored MIT-BIH record into a
feature table. `scripts/train_model.py` compares Logistic Regression, Random
Forest, linear SVM, KNN, and Histogram Gradient Boosting. Splits are grouped by
record, so beats from any one recording never appear in both training and test
data. Median imputation and scaling are fitted inside each model pipeline on
training data only. The selected model is chosen by held-out macro F1.

## Evaluation artifacts

Run `python scripts/evaluate_model.py` after training. It writes actual
record-disjoint metrics, a per-class classification report, a confusion matrix,
and a source-data class distribution chart to `results/`. These artifacts are
the source of truth for the future performance dashboard.

## Model artifact

`heartbeat_model.pkl` is a single saved scikit-learn Pipeline. Its fitted
median imputer and StandardScaler are embedded in the pipeline, preventing a
separate scaler/model version mismatch. Run `python scripts/package_model.py`
to create human-readable `models/model_metadata.json`; run
`python scripts/predict_record.py --record 100` for an end-to-end local
inference smoke test.

## Local prediction API

The Flask backend accepts only UTF-8 `.csv` or `.txt` uploads containing one
numeric ECG-amplitude column and does not retain the uploaded waveform. Use a
multipart `POST /api/predict` with `ecg_file` and optional
`sampling_frequency_hz` (100–1000 Hz; default 360). `GET /api/history` returns
the local SQLite prediction audit list. The 5 MB request cap, strict file
validation, sanitized names, and user-safe errors are applied before inference.

## Quick start (after environment setup)

```powershell
python app.py
```

Then open `http://127.0.0.1:5000` in a browser.
