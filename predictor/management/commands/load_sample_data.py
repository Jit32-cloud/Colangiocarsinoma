from pathlib import Path

from django.core.management.base import BaseCommand

from predictor.forms import PredictionForm
from predictor.ml_service import predict_risk
from predictor.models import PredictionRecord
from predictor.sample_data import SAMPLE_PATIENTS, build_training_dataframe
from predictor.training import train_and_save
from predictor.views import _save_prediction


class Command(BaseCommand):
    help = "Generate sample training CSV, train the model, and seed prediction records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--rows",
            type=int,
            default=200,
            help="Number of synthetic training rows (default: 200).",
        )
        parser.add_argument(
            "--skip-train",
            action="store_true",
            help="Skip CSV generation and model training.",
        )
        parser.add_argument(
            "--skip-seed",
            action="store_true",
            help="Skip inserting sample patient predictions.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing prediction records before seeding.",
        )

    def handle(self, *args, **options):
        artifacts_dir = Path(__file__).resolve().parents[2] / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)
        csv_path = artifacts_dir / "training_data.csv"

        if not options["skip_train"]:
            self.stdout.write(f"Writing synthetic dataset ({options['rows']} rows)...")
            df = build_training_dataframe(options["rows"])
            df.to_csv(csv_path, index=False)
            self.stdout.write(self.style.SUCCESS(f"Saved {csv_path}"))

            self.stdout.write("Training model...")
            train_and_save(str(csv_path))
            self.stdout.write(self.style.SUCCESS("Model trained and saved."))

        if options["skip_seed"]:
            return

        if options["clear"]:
            deleted, _ = PredictionRecord.objects.all().delete()
            self.stdout.write(f"Cleared {deleted} existing record(s).")

        self.stdout.write("Running sample predictions...")
        for payload in SAMPLE_PATIENTS:
            form = PredictionForm(data=payload)
            if not form.is_valid():
                self.stderr.write(self.style.ERROR(f"Invalid sample: {payload['name']}"))
                self.stderr.write(str(form.errors))
                continue

            result = predict_risk(form.cleaned_data)
            record = _save_prediction(form.cleaned_data, result)
            self.stdout.write(
                f"  {record.name}: {record.get_risk_level_display()} "
                f"({result['probability_percent']}%)"
            )

        total = PredictionRecord.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Done. {total} prediction record(s) in database."))
