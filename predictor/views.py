from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import PredictionForm, SignUpForm
from .ml_service import predict_risk
from .models import PredictionRecord

DISCLAIMER_TEXT = (
    "This tool is for educational purposes only and not a substitute for medical advice."
)


def _save_prediction(cleaned_data, result):
    record = PredictionRecord.objects.create(
        name=cleaned_data["name"],
        age=cleaned_data["age"],
        gender=cleaned_data["gender"],
        jaundice=cleaned_data["jaundice"] == "True",
        abdominal_pain=cleaned_data["abdominal_pain"] == "True",
        weight_loss=cleaned_data["weight_loss"] == "True",
        fatigue=cleaned_data["fatigue"] == "True",
        fever=cleaned_data["fever"] == "True",
        bilirubin=cleaned_data["bilirubin"],
        alt=cleaned_data["alt"],
        ast=cleaned_data["ast"],
        alp=cleaned_data["alp"],
        ca19_9=cleaned_data["ca19_9"],
        smoking=cleaned_data["smoking"] == "True",
        alcohol=cleaned_data["alcohol"] == "True",
        diabetes=cleaned_data["diabetes"] == "True",
        liver_disease_history=cleaned_data["liver_disease_history"] == "True",
        gallstones=cleaned_data["gallstones"] == "True",
        risk_level=result["risk_level"],
        probability=result["probability_percent"] / 100.0,
        explanation=result["explanation"],
    )
    return record


def home(request):
    return render(request, "predictor/home.html", {"disclaimer": DISCLAIMER_TEXT})


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("home")

    return render(
        request,
        "predictor/signup.html",
        {"form": form, "disclaimer": DISCLAIMER_TEXT},
    )


@require_http_methods(["GET", "POST"])
def predict(request):
    form = PredictionForm()
    return render(request, "predictor/predict.html", {"form": form, "disclaimer": DISCLAIMER_TEXT})


@require_http_methods(["POST"])
def predict_api(request):
    form = PredictionForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {
                "ok": False,
                "message": "Please fill all fields correctly. Invalid input.",
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    result = predict_risk(form.cleaned_data)
    record = _save_prediction(form.cleaned_data, result)
    payload = {
        "record_id": record.id,
        "name": record.name,
        "risk_level": result["risk_level"],
        "probability_percent": result["probability_percent"],
        "explanation": result["explanation"],
    }
    request.session["result_data"] = payload
    return JsonResponse({"ok": True, "result": payload})


def result(request):
    data = request.session.get("result_data")
    if not data:
        return redirect("predict")
    return render(request, "predictor/result.html", {"result": data, "disclaimer": DISCLAIMER_TEXT})


@login_required
def history(request):
    records = PredictionRecord.objects.all()[:25]
    return render(
        request,
        "predictor/history.html",
        {"records": records, "disclaimer": DISCLAIMER_TEXT},
    )


def report(request):
    data = request.session.get("result_data")
    if not data:
        return redirect("predict")
    return render(request, "predictor/report.html", {"result": data, "disclaimer": DISCLAIMER_TEXT})


def about(request):
    return render(request, "predictor/about.html", {"disclaimer": DISCLAIMER_TEXT})


@require_http_methods(["GET", "POST"])
def contact(request):
    context = {"disclaimer": DISCLAIMER_TEXT}
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        if not name or not email or not message:
            messages.error(request, "Please fill all fields.")
        else:
            messages.success(request, "Message submitted successfully.")
    return render(request, "predictor/contact.html", context)
