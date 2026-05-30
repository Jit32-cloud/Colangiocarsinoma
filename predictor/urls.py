from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("predict/", views.predict, name="predict"),
    path("api/predict/", views.predict_api, name="predict_api"),
    path("result/", views.result, name="result"),
    path("report/", views.report, name="report"),
    path("history/", views.history, name="history"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("login/", auth_views.LoginView.as_view(template_name="predictor/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]
