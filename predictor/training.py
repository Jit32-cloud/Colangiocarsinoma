from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "age",
    "gender",
    "bias",
    "jaundice",
    "abdominal_pain",
    "weight_loss",
    "fatigue",
    "fever",
    "bilirubin",
    "alt",
    "ast",
    "alp",
    "ca19_9",
    "smoking",
    "alcohol",
    "diabetes",
    "liver_disease_history",
    "gallstones",
]
TARGET_COLUMN = "target"


def train_and_save(dataset_path: str):
    dataset = pd.read_csv(dataset_path)
    X = dataset[FEATURE_COLUMNS]
    y = dataset[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)

    output_dir = Path(__file__).resolve().parent / "artifacts"
    output_dir.mkdir(exist_ok=True)
    model_path = output_dir / "cholangio_model.pkl"
    joblib.dump(pipeline, model_path)
    print(f"Model saved at: {model_path}")
    print(f"Validation accuracy: {score:.4f}")


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent / "artifacts" / "training_data.csv"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. Place your CSV there and run again."
        )
    train_and_save(str(data_path))
