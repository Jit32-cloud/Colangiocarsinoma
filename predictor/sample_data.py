"""Synthetic training rows and form-ready sample patients for local testing."""

import numpy as np
import pandas as pd

from .training import FEATURE_COLUMNS, TARGET_COLUMN

RNG = np.random.default_rng(42)


def build_training_dataframe(n_rows: int = 200) -> pd.DataFrame:
    age = RNG.integers(35, 85, size=n_rows)
    gender = RNG.integers(0, 3, size=n_rows)
    bias = np.ones(n_rows)

    jaundice = RNG.integers(0, 2, size=n_rows)
    abdominal_pain = RNG.integers(0, 2, size=n_rows)
    weight_loss = RNG.integers(0, 2, size=n_rows)
    fatigue = RNG.integers(0, 2, size=n_rows)
    fever = RNG.integers(0, 2, size=n_rows)

    bilirubin = RNG.uniform(0.3, 4.0, size=n_rows)
    alt = RNG.uniform(10, 180, size=n_rows)
    ast = RNG.uniform(10, 160, size=n_rows)
    alp = RNG.uniform(40, 350, size=n_rows)
    ca19_9 = RNG.uniform(5, 900, size=n_rows)

    smoking = RNG.integers(0, 2, size=n_rows)
    alcohol = RNG.integers(0, 2, size=n_rows)
    diabetes = RNG.integers(0, 2, size=n_rows)
    liver_disease_history = RNG.integers(0, 2, size=n_rows)
    gallstones = RNG.integers(0, 2, size=n_rows)

    symptom_score = jaundice + abdominal_pain + weight_loss + fatigue + fever
    risk_score = (
        (age / 120.0) * 0.12
        + (bilirubin / 15.0) * 0.15
        + (alt / 200.0) * 0.10
        + (ast / 200.0) * 0.10
        + (alp / 500.0) * 0.12
        + (ca19_9 / 1000.0) * 0.20
        + symptom_score * 0.04
        + (smoking + alcohol + diabetes + liver_disease_history + gallstones) * 0.04
        + RNG.normal(0, 0.05, size=n_rows)
    )
    target = (risk_score >= 0.42).astype(int)

    return pd.DataFrame(
        {
            "age": age,
            "gender": gender,
            "bias": bias,
            "jaundice": jaundice,
            "abdominal_pain": abdominal_pain,
            "weight_loss": weight_loss,
            "fatigue": fatigue,
            "fever": fever,
            "bilirubin": np.round(bilirubin, 2),
            "alt": np.round(alt, 1),
            "ast": np.round(ast, 1),
            "alp": np.round(alp, 1),
            "ca19_9": np.round(ca19_9, 1),
            "smoking": smoking,
            "alcohol": alcohol,
            "diabetes": diabetes,
            "liver_disease_history": liver_disease_history,
            "gallstones": gallstones,
            TARGET_COLUMN: target,
        }
    )[FEATURE_COLUMNS + [TARGET_COLUMN]]


SAMPLE_PATIENTS = [
    {
        "name": "Sample Low Risk",
        "age": 42,
        "gender": "female",
        "jaundice": "False",
        "abdominal_pain": "False",
        "weight_loss": "False",
        "fatigue": "False",
        "fever": "False",
        "bilirubin": 0.8,
        "alt": 28.0,
        "ast": 24.0,
        "alp": 85.0,
        "ca19_9": 18.0,
        "smoking": "False",
        "alcohol": "False",
        "diabetes": "False",
        "liver_disease_history": "False",
        "gallstones": "False",
    },
    {
        "name": "Sample Medium Risk",
        "age": 61,
        "gender": "male",
        "jaundice": "True",
        "abdominal_pain": "True",
        "weight_loss": "False",
        "fatigue": "True",
        "fever": "False",
        "bilirubin": 3.2,
        "alt": 95.0,
        "ast": 88.0,
        "alp": 210.0,
        "ca19_9": 180.0,
        "smoking": "True",
        "alcohol": "False",
        "diabetes": "True",
        "liver_disease_history": "False",
        "gallstones": "True",
    },
    {
        "name": "Sample High Risk",
        "age": 72,
        "gender": "male",
        "jaundice": "True",
        "abdominal_pain": "True",
        "weight_loss": "True",
        "fatigue": "True",
        "fever": "True",
        "bilirubin": 8.5,
        "alt": 160.0,
        "ast": 145.0,
        "alp": 420.0,
        "ca19_9": 650.0,
        "smoking": "True",
        "alcohol": "True",
        "diabetes": "True",
        "liver_disease_history": "True",
        "gallstones": "True",
    },
]
