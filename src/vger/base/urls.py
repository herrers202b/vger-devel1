from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView.as_view(), name='survey'),
    path('survey/<slug:surveySlug>', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('', views.home, name='home-page'),
    path('survey/create/', views.SurveyCreate.as_view(), name='survey-create'),
    path('survey/<slug:surveySlug>/update/', views.SurveyUpdate.as_view(), name='survey-update'),
    path('survey/<slug:surveySlug>/delete/', views.SurveyDelete.as_view(), name='survey-delete'),
    path('survey/<slug:surveySlug>/create-category/', views.CategoryCreate.as_view(), name='category-create'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>update-category/', views.CategoryUpdate.as_view(), name='category-update'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>delete-category/', views.CategoryDelete.as_view(), name='category-delete'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>/create-question/', views.QuestionCreate.as_view(), name='question-create'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>/Question/<slug:questionSlug>', views.QuestionDetailView.as_view(), name='question-detail'),
]
