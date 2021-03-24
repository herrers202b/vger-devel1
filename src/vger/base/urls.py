from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView.as_view(), name='survey'),
    path('survey/<int:pk>', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('', views.home, name='home-page'),
    # needs hash symbol
    path('survey/results/', views.results, name='results-page')
]
