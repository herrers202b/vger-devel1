from django.urls import path
from . import views

urlpatterns = [
    path('survey/', views.SurveyListView, name='survey'),
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
    path('survey/<slug:surveySlug>/category/<int:categoryPk>/question/<int:pk>', views.QuestionDetailView.as_view(), name='question-detail'),
    path('survey/<slug:surveySlug>/category/<int:categoryPk>/question/<int:pk>/update-question/', views.QuestionUpdate.as_view(), name='question-update'),
    path('survey/<slug:surveySlug>/category/<int:categoryPk>/question/<int:pk>/delete-question/', views.QuestionDelete.as_view(), name='question-delete'),
    path('options/create', views.CreateChoice, name='option-create'),
    path('options/update/<int:pk>', views.OptionUpdateView.as_view(), name='option-update'),
    path('options/delete/<int:pk>', views.OptionDeleteView.as_view(), name='option-delete'),
    path('options/list', views.OptionListView, name='option-list'),
    path('options/detail/<int:pk>', views.OptionDetailView.as_view(), name='option-detail'),
    path('options/choice-update/<int:pk>', views.ChoiceUpdate.as_view(), name='choice-update'),
    path('options/choice-delete/<int:pk>', views.ChoiceDelete.as_view(), name='choice-create'),
    path('survey/results/<slug:surveySlug>/<int:pk>', views.results, name='results-page'),
    path('survey/take/<slug:surveySlug>', views.generateNewSurvey, name='gen-survey'),
    path('survey/welcome/<slug:surveySlug>', views.welcomeSurvey, name='welcome-to-survey'),
    path('survey/take/<slug:surveySlug>/page=<int:page>', views.takeSurvey, name='take-survey'),
    path('survey/<slug:surveySlug>/<str:version_number>/new-version', views.newVersion, name='new-version')
]
