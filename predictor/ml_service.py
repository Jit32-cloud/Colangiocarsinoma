from pathlib import Path
from typing import Dict, List

import joblib
import numpy as np
from django.conf import settings


class DummyRiskModel:
    """Fallback model so the app works before training."""

    def predict_proba(self, X):
        rows = np.array(X, dtype=float)
        probs = []
        for row in rows:
            symptom_score = np.sum(row[3:8])
            risk_score = (
                (row[0] / 120.0) * 0.12
                + (row[8] / 15.0) * 0.15
                + (row[9] / 200.0) * 0.10
                + (row[10] / 200.0) * 0.10
                + (row[11] / 500.0) * 0.12
                + (row[12] / 1000.0) * 0.20
                + symptom_score * 0.04
                + np.sum(row[13:18]) * 0.04
            )
            prob = float(max(0.02, min(0.98, risk_score)))
            probs.append([1 - prob, prob])
        return np.array(probs)


def _model_path() -> Path:
    return settings.BASE_DIR / "predictor" / "artifacts" / "cholangio_model.pkl"


def load_model():
    model_file = _model_path()
    if model_file.exists():
        return joblib.load(model_file)
    return DummyRiskModel()


def build_feature_vector(cleaned_data: Dict) -> List[float]:
    gender_map = {"male": 0.0, "female": 1.0, "other": 2.0}
    return [
        float(cleaned_data["age"]),
        gender_map.get(cleaned_data["gender"], 2.0),
        1.0,
        float(cleaned_data["jaundice"] == "True"),
        float(cleaned_data["abdominal_pain"] == "True"),
        float(cleaned_data["weight_loss"] == "True"),
        float(cleaned_data["fatigue"] == "True"),
        float(cleaned_data["fever"] == "True"),
        float(cleaned_data["bilirubin"]),
        float(cleaned_data["alt"]),
        float(cleaned_data["ast"]),
        float(cleaned_data["alp"]),
        float(cleaned_data["ca19_9"]),
        float(cleaned_data["smoking"] == "True"),
        float(cleaned_data["alcohol"] == "True"),
        float(cleaned_data["diabetes"] == "True"),
        float(cleaned_data["liver_disease_history"] == "True"),
        float(cleaned_data["gallstones"] == "True"),
    ]


def predict_risk(cleaned_data: Dict):
    model = load_model()
    feature_vector = build_feature_vector(cleaned_data)
    probability = float(model.predict_proba([feature_vector])[0][1])
    percent = round(probability * 100, 2)

    if percent < 35:
        risk_level = "low"
        explanation = "Risk indicators are currently in a lower range."
    elif percent < 70:
        risk_level = "medium"
        explanation = "Some indicators are elevated. Medical review is advised."
    else:
        risk_level = "high"
        explanation = "Several indicators are elevated. Seek prompt clinical evaluation."

    return {
        "risk_level": risk_level,
        "probability_percent": percent,
        "explanation": explanation,
        "feature_vector": feature_vector,
    }
