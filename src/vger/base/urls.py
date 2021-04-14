from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView.as_view(), name='survey'),
    # path('survey/<slug:surveySlug>', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('survey/<slug:surveySlug>', views.SureveyDetailView, name='survey-detail'),
    path('', views.home, name='home-page'),
    path('survey/create/', views.SurveyCreate.as_view(), name='survey-create'),
    path('survey/<slug:surveySlug>/update/', views.SurveyUpdate.as_view(), name='survey-update'),
    path('survey/<slug:surveySlug>/delete/', views.SurveyDelete.as_view(), name='survey-delete'),
    path('survey/<slug:surveySlug>/create-category/', views.CategoryCreate.as_view(), name='category-create'),
    path('survey/<slug:surveySlug>/category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('survey/<slug:surveySlug>/category/<int:pk>/update-category/', views.CategoryUpdate.as_view(), name='category-update'),
    path('survey/<slug:surveySlug>/category/<int:pk>/delete-category/', views.CategoryDelete.as_view(), name='category-delete'),
    path('survey/<slug:surveySlug>/category/<int:pk>/create-question/', views.QuestionCreate.as_view(), name='question-create'),
    path('survey/<slug:surveySlug>/category/<int:categoryPk>/<int:sQPk>/question/<int:questionPk>', views.QuestionDetailView.as_view(), name='question-detail'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>/question/<slug:questionSlug>/update-question/', views.QuestionUpdate.as_view(), name='question-update'),
    path('survey/<slug:surveySlug>/category/<slug:categorySlug>/question/<slug:questionSlug>/delete-question/', views.QuestionDelete.as_view(), name='question-delete'),
    path('survey/results/<slug:surveySlug>', views.results, name='results-page'),
    path('survey/take/<slug:surveySlug>', views.generateNewSurvey, name='gen-survey'),
    path('survey/welcome/<slug:surveySlug>', views.welcomeSurvey, name='welcome-to-survey'),
    path('survey/take/<slug:surveySlug>/page=<int:page>', views.takeSurvey, name='take-survey')
]
