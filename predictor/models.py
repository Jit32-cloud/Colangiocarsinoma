from django.db import models


class PredictionRecord(models.Model):
    RISK_LOW = "low"
    RISK_MEDIUM = "medium"
    RISK_HIGH = "high"
    RISK_CHOICES = [
        (RISK_LOW, "Low"),
        (RISK_MEDIUM, "Medium"),
        (RISK_HIGH, "High"),
    ]

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    jaundice = models.BooleanField()
    abdominal_pain = models.BooleanField()
    weight_loss = models.BooleanField()
    fatigue = models.BooleanField()
    fever = models.BooleanField()

    bilirubin = models.FloatField()
    alt = models.FloatField()
    ast = models.FloatField()
    alp = models.FloatField()
    ca19_9 = models.FloatField()

    smoking = models.BooleanField()
    alcohol = models.BooleanField()
    diabetes = models.BooleanField()
    liver_disease_history = models.BooleanField()
    gallstones = models.BooleanField()

    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES)
    probability = models.FloatField()
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.get_risk_level_display()} ({self.created_at:%Y-%m-%d})"
