from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView.as_view(), name='survey'),
    path('survey/<int:pk>', views.SurveyDetailView.as_view(), name='survey-detail'),
]