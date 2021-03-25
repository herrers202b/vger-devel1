from django.shortcuts import render
#Form imports
from base.forms import SurveyModelFrom, CategoryModelForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.text import slugify
#Authentication imports
from django.contrib.auth.decorators import login_required, permission_required
#Generic imports
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#Model imports
from .models import Survey, Category, Question, SurveyInstance

# Create your views here.

class SurveyListView(generic.ListView):
    """
    SurveyListView

    This class lists all currently registered 
    surveys on the website.

    Parameters
    ----------
    Survey : model
        The specific model we're trying to list
    'survey_list' : context_object_name
        this is what we will refer to when trying
        to query via HTML
    'survey_list.html'
        the name of our html file that contains
        the template we will use
    """
    model = Survey
    context_object_name = 'survey_list'
    template_name = 'survey_list.html' 

class SurveyDetailView(generic.DetailView):
    """
    SurveyDetailView

    This is the class that we will use to show
    the details of a specific survey

    Survey : model
        The specific model we will be detailing in this view
    
    'survey_detail' :  context_object_name
        this is what we will refer to when trying
        to query via HTML

    'survey_detail.html' : template_name
        the name of our html file that contains
        the template we will use

    'surveySlug' : slug_field
        slug field for this view

    'surveySlug' : slug_url_kwarg
        slug keyword arguments for this view
    
    """
    from django.shortcuts import get_object_or_404

    model = Survey
    context_object_name = 'survey_detail'
    template_name = 'survey_detail.html' 
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'

    def survey_detail_view(request, primary_key):
        """
        survey_detail_view

        Method, adapted from Django tutorial, will check
        to see if a survey exists.

        Survey : the obeject we will either retrieve 
            or 404 error
        
        method returns the appropriate render
        """
        Survey = get_object_or_404(Survey, slug=slug) 
        return render(request, 'base/templates/survey_detail.html', context={'survey': Survey})

class CategoryDetailView(generic.DetailView):
    """
    CategoryDetailView

    Class used to show the specific details of a given category

    Category : model
        the model we will use for this class
    
    'category_detail' : context_object_name
        the name we reference when querying the html

    'category_detail.html' : template_name
        the name of the template we are using
        to generate this view

    'categorySlug' : slug_field
        slug field for this view

    'categorySlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    from django.shortcuts import get_object_or_404

    model = Category
    context_object_name = 'category_detail'
    template_name = 'category_detail.html'
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'

    def category_detail_view(request, primary_key):
        """
        category_detail_view

        Method, adapted from Django tutorial, will check
        to see if a category exists.

        Category : the obeject we will either retrieve 
            or 404 error
        
        method returns the appropriate render
        """
        Category = get_object_or_404(Category, slug=slug)
        return render(request, 'base/templates/category_detail.html', context={'category': category})

class QuestionDetailView(generic.DetailView):
    """
    QuestionDetailView

    Class used to show the specific details of a given question

    Question : model
        the model we will use for this class
    
    'question_detail' : context_object_name
        the name we reference when querying the html

    'question_detail.html' : template_name
        the name of the template we are using
        to generate this view

    'questionSlug' : slug_field
        slug field for this view

    'questionSlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    from django.shortcuts import get_object_or_404

    model = Question
    context_object_name = 'question_detail'
    template_name = 'question_detail.html'
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'

    def question_detail_view(request, primary_key):
        """
        question_detail_view

        Method, adapted from Django tutorial, will check
        to see if a question exists.

        Question : the obeject we will either retrieve 
            or 404 error
        
        method returns the appropriate render
        """
        Question = get_object_or_404(Category, slug=slug)
        return render(request, 'base/templates/question_detail.html', context={'question': question})

#HTML Render request?
def home(request):
    return render(request, 'home.html')

#Class templated for creating, updating, and deleting surveys
#Still needs permissions!
class SurveyCreate(CreateView):
    """
    SurveyCreate View
    
    Method builds off the generics provided by django to
    offer a user the ability to create a survey

    Survey : model
        Survey is the model used in this form

    survey_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'surveySlug' : slug_field
        slug field for this view

    'surveySlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    model = Survey
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'
    fields = ['titleOfSurvey', 'directions']
    template_name = 'survey_form.html' 

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('survey-detail', kwargs={'surveySlug': self.object.surveySlug})        

class SurveyUpdate(UpdateView):
    """
    SurveyUpdate View
    
    Method builds off the generics provided by django to
    offer a user the ability to update a survey

    Survey : model
        Survey is the model used in this form
    
    survey_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'surveySlug' : slug_field
        slug field for this view

    'surveySlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    model = Survey
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'
    fields = ['titleOfSurvey', 'directions']
    template_name = 'survey_form.html' 

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('survey-detail', kwargs={'surveySlug': self.object.surveySlug})

class SurveyDelete(DeleteView):
    """
    SurveyDelete View
    
    Method builds off the generics provided by django to
    offer a user the ability to delete a survey. 
    On submission we go back to the survey list page
    On cancel we return to the previous window

    Survey : model
        Survey is the model used in this form
    
    survey_form_confirm_delete.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'surveySlug' : slug_field
        slug field for this view

    'surveySlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    model = Survey
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'
    template_name = 'survey_form_confirm_delete.html' 
    #forgo success url method since we are at the top of the tree
    success_url = reverse_lazy('survey')

#Class templated for creating, updating, and deleting categories
#Still needs permissions!
class CategoryCreate(CreateView):
    """
    CategoryCreate View
    
    Method builds off the generics provided by django to
    offer a user the ability to create a category. 

    Category : model
        Category is the model used in this form
    
    category_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'categorySlug' : slug_field
        slug field for this view

    'categorySlug' : slug_url_kwarg
        slug keyword arguments for this view
    """    
    model = Category
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    template_name = 'category_form.html'
    fields = ['titleOfCategory','lowWeightText', 'highWeightText']

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('category-detail', kwargs={'surveySlug': self.object.survey.surveySlug,
                                                    'categorySlug': self.object.categorySlug})
    
    def form_valid(self, form):
        """
        form_valid

        This method is used on HTTP Post,
        we will set our 'Parent Survey' to that
        of the survey passed in with our kwargs
        """

        form.instance.survey = Survey.objects.get(surveySlug=self.kwargs['surveySlug'])
        return super(CategoryCreate, self).form_valid(form)
        

class CategoryUpdate(UpdateView):
    """
    CategoryUpdate View
    
    Method builds off the generics provided by django to
    offer a user the ability to update a category

    Category : model
        Category is the model used in this form
    
    category_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.
    
    'categorySlug' : slug_field
        slug field for this view

    'categorySlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    model = Category
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    template_name = 'category_form.html'
    fields = ['titleOfCategory','lowWeightText', 'highWeightText']

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('category-detail', kwargs={'surveySlug': self.object.survey.surveySlug,
                                                    'categorySlug': self.object.categorySlug}) 

class CategoryDelete(DeleteView):
    """
    CategoryDelete View
    
    Method builds off the generics provided by django to
    offer a user the ability to delete a category. 
    On submission we go back to the survey detail page
    On cancel we return to the previous window

    Category : model
        Category is the model used in this form
    
    category_form_confirm_delete.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'categorySlug' : slug_field
        slug field for this view

    'categorySlug' : slug_url_kwarg
        slug keyword arguments for this view
    
    """
    model = Category
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    template_name = 'category_form_confirm_delete.html' 

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('survey-detail', kwargs={'surveySlug': self.object.survey.surveySlug})
    success_url = get_success_url

class QuestionCreate(CreateView):
    """
    QuestionCreate View
    
    Method builds off the generics provided by django to
    offer a user the ability to create a question. 

    Question : model
        Question is the model used in this form
    
    question_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'questionSlug' : slug_field
        slug field for this view

    'questionSlug' : slug_url_kwarg
        slug keyword arguments for this view
    """    
    model = Question
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    template_name = 'question_form.html'
    fields = ['questionText','answer', 'questionNumber']

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('question-detail', kwargs={'surveySlug': self.object.category.survey.surveySlug,
                                                    'categorySlug': self.object.category.categorySlug,
                                                    'questionSlug': self.object.questionSlug})
    
    def form_valid(self, form):
        """
        form_valid

        This method is used on HTTP Post,
        we will set our 'Parent Category' to that
        of the survey passed in with our kwargs
        """
        form.instance.category = Category.objects.get(categorySlug=self.kwargs['categorySlug'])
        return super(QuestionCreate, self).form_valid(form)

class QuestionUpdate(UpdateView):
    """
    QuestionUpdate View
    
    Method builds off the generics provided by django to
    offer a user the ability to update a category

    Question : model
        Question is the model used in this form
    
    question_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'questionSlug' : slug_field
        slug field for this view

    'questionSlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    model = Question
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    template_name = 'question_form.html'
    fields = ['questionText','answer', 'questionNumber']

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('question-detail', kwargs={'surveySlug': self.object.category.survey.surveySlug,
                                                    'categorySlug': self.object.category.categorySlug,
                                                    'questionSlug': self.object.questionSlug})

class QuestionDelete(DeleteView):
    """
    QuestionDelete View
    
    Method builds off the generics provided by django to
    offer a user the ability to delete a question. 
    On submission we go back to the category detail page
    On cancel we return to the previous window

    Question : model
        Question is the model used in this form
    
    question_form_confirm_delete.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.
    
    'questionSlug' : slug_field
        slug field for this view

    'questionSlug' : slug_url_kwarg
        slug keyword arguments for this view
    """
    model = Question
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    template_name = 'question_form_confirm_delete.html' 
    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('category-detail', kwargs={'surveySlug': self.object.category.survey.surveySlug,
                                                    'categorySlug': self.object.category.categorySlug})
    success_url = get_success_url