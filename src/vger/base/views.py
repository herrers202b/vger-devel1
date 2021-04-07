from django.db.models.query import QuerySet
from django.shortcuts import render
#Form imports
# from base.forms import SurveyModelFrom, CategoryModelForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.text import slugify
#Authentication imports
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#Generic imports
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
#User imports
from user.models import Administrator, Advisor, Student
#Model imports
from .models import Survey, Category, Survey_Question, Answer, Question, Option_Choice, Option_Group, Input_Type
from django.shortcuts import redirect
# from .forms import SurveyCategoryForm


import hashlib, random, sys


# Create your views here.
def check_permissions(request, accountType, url):
    """
    check_permissions

    Queries for all of one type of user and checks them against the current user.
    If the user is authenticated they are directed to the page they were 
    looking for. Otherwise they are told they do not have permission to view the page.
    """
    if not request.user.is_authenticated:
            return redirect('/login/')
    if accountType == Advisor:
        advisory_query = Advisor.objects.all()
        for advisor in advisory_query:
            if advisor.user == request.user:
                return render(request, url)
        return HttpResponseNotAllowed('<h1>You do not have permission to access this page</h1>')
    elif accountType == Administrator:
        admin_query = Administrator.objects.all()
        for admin in admin_query:
            if admin.user == request.user:
                return render(request, url)
        return HttpResponseNotAllowed('<h1>You do not have permission to access this page</h1>')
    else:
        student_query = Student.objects.all()
        for student in student_query:
            if student.user == request.user:
                return render(request, url)
        return HttpResponseNotAllowed('<h1>You do not have permission to access this page</h1>')

class SurveyListView(LoginRequiredMixin, generic.ListView):
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
    '/login/' 
        redirect url for login required permission
    """
    model = Survey
    context_object_name = 'survey_list'
    template_name = 'survey_list.html' 
    login_url = '/login/'

# class SurveyDetailView(LoginRequiredMixin, request):
#     """
#     SurveyDetailView

#     This is the class that we will use to show
#     the details of a specific survey

#     Survey : model
#         The specific model we will be detailing in this view
    
#     'survey_detail' :  context_object_name
#         this is what we will refer to when trying
#         to query via HTML

#     'survey_detail.html' : template_name
#         the name of our html file that contains
#         the template we will use

#     'surveySlug' : slug_field
#         slug field for this view

#     'surveySlug' : slug_url_kwarg
#         slug keyword arguments for this view
        
#     '/login/' 
#         redirect url for login required permission
#     """
#     from django.shortcuts import get_object_or_404
#     model = Survey
#     context_object_name = 'survey_detail'
#     template_name = 'survey_detail.html' 
#     slug_field = 'surveySlug'
#     slug_url_kwarg = 'surveySlug'
#     login_url = '/login/'
    

#     def survey_detail_view(self, request, primary_key):
#         """
#         survey_detail_view

#         Method, adapted from Django tutorial, will check
#         to see if a survey exists.

#         Survey : the obeject we will either retrieve 
#             or 404 error
        
#         method returns the appropriate render
            
#         '/login/' 
#             redirect url for login required permission
#         """
#         Survey = get_object_or_404(Survey, slug=slug)
#         return render(request, 'base/templates/survey_detail.html', context={'survey': Survey})
from .forms import CategoryCreateForm

def SureveyDetailView(request, surveySlug):
    if not request.user.is_authenticated:
         return redirect('/login/')
    
    survey = Survey.objects.get(surveySlug=surveySlug)
    categories = Category.objects.filter(survey_fk=survey)
    questions = Survey_Question.objects.filter(survey_fk=survey)
    
    #category_form = CategoryCreateForm()
    context = {
        'survey' : survey,
        'categories' : categories,
        'questions' : questions,
    }
    
    return render(request, 'survey_detail.html', context)
    

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
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
    
    '/login/' 
        redirect url for login required permission    
    """
    from django.shortcuts import get_object_or_404

    model = Category
    context_object_name = 'category_detail'
    template_name = 'category_detail.html'
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    login_url = '/login/'

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
        return render(request, 'base/templates/category_detail.html', context={'category': Category})

class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
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

    '/login/' 
        redirect url for login required permission 
    """
    from django.shortcuts import get_object_or_404

    model = Question
    context_object_name = 'question_detail'
    template_name = 'question_detail.html'
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    login_url = '/login/'

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

def home(request):
    return render(request, 'home.html')

#Class templated for creating, updating, and deleting surveys
from .forms import SurveyCreateForm

class SurveyCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
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

    '/login/' 
        redirect url for login required permission 
    
    'canCreateSurvey' : permission_required
        Permission requirement to use this view
    """
    model = Survey
    form_class = SurveyCreateForm
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'
    login_url = '/login/'
    permission_required = 'canCreateSurvey'

    def get(self, request, *args, **kwargs):
        context = {'form': SurveyCreateForm()}
        return render(request, 'survey_form.html', context)

    def form_valid(self, form):
        survey = form.save()
        survey.save()
        return redirect(reverse('survey-detail', kwargs={'surveySlug': survey.surveySlug}))
            

class SurveyUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    SurveyUpdate View
    
    Method builds off the generics provided by django to
    offer a user the ability to update a survey
    survey_form.html : template_name
        The name of the template we want Djagno 
        to use when creating this view.

    'surveySlug' : slug_field
        slug field for this view

    'surveySlug' : slug_url_kwarg
        slug keyword arguments for this view

    '/login/' 
        redirect url for login required permission 

    'canUpdateSurvey' : permission_required
        Permission requirement to use this view
    """
    model = Survey
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'
    fields = ['titleOfSurvey', 'description']
    template_name = 'survey_form.html'
    login_url = '/login/' 
    permission_required = 'canUpdateSurvey'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('survey-detail', kwargs={'surveySlug': self.object.surveySlug})

class SurveyDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
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

    '/login/' 
        redirect url for login required permission 

    'canDeleteSurvey' : permission_required
        Permission requirement to use this view
    """
    model = Survey
    slug_field = 'surveySlug'
    slug_url_kwarg = 'surveySlug'
    template_name = 'survey_form_confirm_delete.html' 
    #forgo success url method since we are at the top of the tree
    success_url = reverse_lazy('survey')
    login_url = '/login/'
    permission_required = 'canDeleteSurvey'


#Class templated for creating, updating, and deleting categories
#Still needs permissions!
class CategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
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

    '/login/' 
        redirect url for login required permission 

    'canCreateCategory' : permission_required
        Permission requirement to use this view
    """    
    model = Category
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    template_name = 'category_form.html'
    fields = ['titleOfCategory',]
    login_url = '/login/'
    permission_required = 'canCreateCategory'
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
        

class CategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
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

    '/login/' 
        redirect url for login required permission 

    'canUpdateCategory' : permission_required
        Permission requirement to use this view
    """
    model = Category
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    template_name = 'category_form.html'
    fields = ['titleOfCategory',]
    login_url = '/login/'
    permission_required = 'canUpdateCategory'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('category-detail', kwargs={'surveySlug': self.object.survey.surveySlug,
                                                    'categorySlug': self.object.categorySlug}) 

class CategoryDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
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

    '/login/' 
        redirect url for login required permission 
    
    'canDeleteCategory' : permission_required
        Permission requirement to use this view
    """
    model = Category
    slug_field = 'categorySlug'
    slug_url_kwarg = 'categorySlug'
    template_name = 'category_form_confirm_delete.html' 
    login_url = '/login/'
    permission_required = 'canDeleteCategory'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('survey-detail', kwargs={'surveySlug': self.object.survey.surveySlug})
    success_url = get_success_url

class QuestionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
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

    '/login/' 
        redirect url for login required permission 

    'canCreateQuestion' : permission_required
        Permission requirement to use this view
    """    
    model = Question
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    template_name = 'question_form.html'
    fields = ['questionText','answer', 'questionNumber']
    login_url = '/login/'
    permission_required = 'canCreateQuestion'

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
        print(form.cleaned_data)
        return super(QuestionCreate, self).form_valid(form)
        

class QuestionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
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

    '/login/' 
        redirect url for login required permission 
    
    'canUpdateQuestion' : permission_required
        Permission requirement to use this view
    """
    model = Question
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    template_name = 'question_form.html'
    fields = ['questionText','answer', 'questionNumber']
    login_url = '/login/'
    permission_required = 'canUpdateQuestion'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('question-detail', kwargs={'surveySlug': self.object.category.survey.surveySlug,
                                                    'categorySlug': self.object.category.categorySlug,
                                                    'questionSlug': self.object.questionSlug})

class QuestionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
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

    '/login/' 
        redirect url for login required permission 

    'canDeleteQuestion' : permission_required
        Permission requirement to use this view
    """
    model = Question
    slug_field = 'questionSlug'
    slug_url_kwarg = 'questionSlug'
    template_name = 'question_form_confirm_delete.html' 
    login_url = '/login/'
    permission_required = 'canDeleteQuestion'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('category-detail', kwargs={'surveySlug': self.object.category.survey.surveySlug,
                                                    'categorySlug': self.object.category.categorySlug})
    # success_url = get_success_url
    
###############################################################################
def create_session_hash():
            hash = hashlib.sha1()
            hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
            return hash.hexdigest()

#This func is used to handle a survey object and count the number of necessary pages
#and then pass that data pack in a representable way to be handled in either a session
#based format or in some itterative represenation
def survey_page_counter(survey):
    return len(Category.objects.filter(survey_fk=survey))

##############################################################################33
from .models import User_Survey
def generateNewSurvey(request, surveySlug):
    #TODO: need to check if user had a survey
    if not request.user.is_authenticated:
        return redirect('/login/')

    survey = Survey.objects.get(surveySlug=surveySlug)    
    request.session['surveySlug'] = surveySlug
    request.session['totalPage'] = survey_page_counter(survey)
    request.session['currPage'] = 0

    u_s = User_Survey.objects.create(user_fk=request.user, survey_fk=survey)
    u_s.save()
    return redirect(survey.get_take_url())

def welcomeSurvey(request, surveySlug):
    #TODO: need to check if user had a survey
    if not request.user.is_authenticated:
        return redirect('/login/')

    survey = Survey.objects.get(surveySlug=surveySlug)
    context = {
         'Survey' : survey,
    }
    return render(request, 'welcome_to_survey.html', context)

from .forms import SurveyCategoryForm

def takeSurvey(request, surveySlug, page):
    #TODO: need to check if user had a survey in User_Survey
    currPage = request.session.get('currPage', 0)
    totalPage = request.session.get('totalPage', 0)
    survey = Survey.objects.get(surveySlug=request.session.get('surveySlug')) 
    list_of_categories = Category.objects.filter(survey_fk=survey)[::1]
    
    if currPage == totalPage:
            return redirect('results-page')

    if request.method == 'POST':
        form = SurveyCategoryForm(request.POST, instance=list_of_categories[currPage].pk)
        if form.is_valid():
            #TODO: Save answers of all types rather than just radio
            for (q, a) in form.category_answers():
                answer = Answer.objects.create(
                    user_fk = request.user,
                    survey_question_fk = Survey_Question.objects.get(pk=q),
                    answer_text = a
                )
                answer.save()

            request.session['currPage'] = currPage + 1
        
        if currPage + 1 == totalPage:
            return redirect('results-page')

    
    form = SurveyCategoryForm(instance=list_of_categories[currPage].pk)
    
    context = {
        'toc' : list_of_categories[currPage].titleOfCategory,
        'form' : form,
    }
    print("here")
    return render(request, 'take_survey.html', context)

# def results(request, session_hash):
#     """
#     results

#     num_instances : the object will return the number of 
#         times user has taken survey 
#     """
#     context_object_name = 'results-page'
#     template_name = 'results.html'

#     si = SurveyInstance.objects.get(session_hash=session_hash)
#     survey_name = si.survey.titleOfSurvey
#     categories = Category.objects.filter(survey=si.survey)
#     questions = []
#     for category in categories: 
#         questions += list(Question.objects.filter(category=category))

#     context = {
#         'Name_of_survey': survey_name,
#         'instance_hash': si,
#         'categories': categories,
#         'questions': questions,
#     }
#     return render(request, 'results.html', context=context)
