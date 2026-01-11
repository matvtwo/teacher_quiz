from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tests/", views.tests, name="tests"),
    path("t/<int:test_id>/", views.take_test, name="take_test"),
]

from .views_ai import generate_questions_async
urlpatterns += [
    path("admin/ai/generate-questions/", generate_questions_async),
]