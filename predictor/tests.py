from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .forms import PredictionForm
from .ml_service import predict_risk
from .models import PredictionRecord
from .sample_data import SAMPLE_PATIENTS, build_training_dataframe
from .training import train_and_save
from .views import _save_prediction


class SampleDataTests(TestCase):
    def setUp(self):
        from pathlib import Path

        artifacts_dir = Path(__file__).resolve().parent / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)
        csv_path = artifacts_dir / "training_data_test.csv"
        build_training_dataframe(120).to_csv(csv_path, index=False)
        train_and_save(str(csv_path))

    def test_training_dataframe_shape(self):
        df = build_training_dataframe(50)
        self.assertEqual(len(df), 50)
        self.assertIn("target", df.columns)

    def test_sample_patients_validate(self):
        for payload in SAMPLE_PATIENTS:
            form = PredictionForm(data=payload)
            self.assertTrue(form.is_valid(), msg=form.errors)

    def test_predict_risk_returns_expected_keys(self):
        form = PredictionForm(data=SAMPLE_PATIENTS[0])
        form.is_valid()
        result = predict_risk(form.cleaned_data)
        self.assertIn(result["risk_level"], ("low", "medium", "high"))
        self.assertGreaterEqual(result["probability_percent"], 0)
        self.assertLessEqual(result["probability_percent"], 100)

    def test_save_prediction_creates_record(self):
        form = PredictionForm(data=SAMPLE_PATIENTS[1])
        form.is_valid()
        result = predict_risk(form.cleaned_data)
        before = PredictionRecord.objects.count()
        _save_prediction(form.cleaned_data, result)
        self.assertEqual(PredictionRecord.objects.count(), before + 1)

    def test_predict_api_accepts_sample_payload(self):
        client = Client()
        response = client.post(reverse("predict_api"), data=SAMPLE_PATIENTS[2])
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["ok"])
        self.assertIn(body["result"]["risk_level"], ("low", "medium", "high"))

    def test_logout_requires_post(self):
        user = User.objects.create_user(username="logouttest", password="testpass123")
        client = Client()
        client.login(username="logouttest", password="testpass123")

        get_response = client.get(reverse("logout"))
        self.assertEqual(get_response.status_code, 405)

        post_response = client.post(reverse("logout"))
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(post_response.wsgi_request.user.is_authenticated)

    def test_risk_levels_span_samples(self):
        levels = set()
        for payload in SAMPLE_PATIENTS:
            form = PredictionForm(data=payload)
            form.is_valid()
            levels.add(predict_risk(form.cleaned_data)["risk_level"])
        self.assertGreaterEqual(len(levels), 2)
