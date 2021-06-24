from django.urls import path

from . import views

urlpatterns = [
    path('<int:client_id>/books', views.ClientBookView.as_view()),
]
