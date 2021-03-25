from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView.as_view(), name='survey'),
    path('survey/<int:pk>', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('', views.home, name='home-page'),
    path('survey/take/<int:pk>', views.generateNewSurvey, name='gen-survey'),
    path('survey/take/<slug:session_hash>', views.welcomeSurvey, name='welcome-to-survey'),
    path('survey/take/<slug:session_hash>/page=<int:page>', views.takeSurvey, name='take-survey')
]
