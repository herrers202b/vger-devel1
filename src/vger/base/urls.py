from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView.as_view(), name='survey'),
    path('survey/<int:pk>', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('', views.home, name='home-page'),
    path('survey/create/', views.SurveyCreate.as_view(), name='survey-create'),
    path('survey/<int:pk>/update/', views.SurveyUpdate.as_view(), name='survey-update'),
    path('survey/<int:pk>/delete/', views.SurveyDelete.as_view(), name='survey-delete'),
]
