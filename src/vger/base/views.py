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

def SurveyListView(request):

    context = {
        'survey_list' : Survey.objects.all()
    }

    return render(request, "survey_list.html", context)

from .forms import NewVersionForm

def newVersion(request, surveySlug, version_number):
    survey = Survey.objects.get(surveySlug=surveySlug)
    if request.method == 'POST':
        form = NewVersionForm(request.POST)
        if form.is_valid():
            new_version_number = form.cleaned_data.get('version_number')
            version_numbers = Survey.objects.filter(titleOfSurvey=survey.titleOfSurvey)
            for number in version_numbers:
                if number.version_number == new_version_number:
                    form = NewVersionForm()
                    context = {
                    'form' : form,
                    'version_numbers': version_numbers
                    }
                    return render(request, "new_version.html", context)
            survey.surveySlug = survey.titleOfSurvey + str(new_version_number).split('.')[0] + str(new_version_number).split('.')[1]
            survey.version_number = new_version_number
            survey.pk = None
            
            survey.save()

            
    else:
        form = NewVersionForm()
        

        version_numbers = Survey.objects.filter(titleOfSurvey=survey.titleOfSurvey)

    context = {
        'form' : form,
        'version_numbers': version_numbers
    }
    return render(request, "new_version.html", context)

from .forms import CategoryCreateForm
@permission_required('canSeeSurveyDetail')
def SureveyDetailView(request, surveySlug):
    """
    Survey Detail View

    This method takes a request and key(surveySlug) and returns
    a render of the survey detail view

    survey, categories, questions : objects
        Objects that are returned from queries and then
        passed as context to HTML templates

    context : context
        list of queries that will
         be sent to HTML templates

    """
    #Login check
    if not request.user.is_authenticated:
         return redirect('/login/')
    #Permission check
    permission_required = 'canSeeSurveyDetail'
    survey = Survey.objects.get(surveySlug=surveySlug)
    categories = Category.objects.filter(survey_fk=survey)
    questions = Survey_Question.objects.filter(survey_fk=survey)

    context = {
        'survey' : survey,
        'categories' : categories,
        'questions' : questions,
    }

    return render(request, 'survey_detail.html', context)

class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin ,generic.DetailView):
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

    '/login/'
        redirect url for login required permission
    """
    from django.shortcuts import get_object_or_404

    model = Category
    context_object_name = 'category_detail'
    template_name = 'category_detail.html'
    login_url = '/login/'
    permission_required = 'canSeeCategoryDetail'

    def get_context_data(self, **kwargs):
        """
        get_context_data

        Method overrides base get_context_view method. This
        method is used to gather objects that are then
        cataloged into a context tuple. Said tuple will be
        sent to HTML templates

        self.object : object
            database object

        this_category : Category
            A category object that will be passed to HTML

        myQuestions : Queryset
            a queryset of questions that will be passed to HTML
        """
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        this_category = Category.objects.get(pk=self.object.pk)
        context['categories'] = this_category

        from django.core.exceptions import ObjectDoesNotExist

        try:
            myQuestions = Question.objects.filter(survey_questions__category_fk=this_category)
            context['myQuestions'] = myQuestions
        except Survey_Question.DoesNotExist:
            myQuestions = None
        return context

    def category_detail_view(request, primary_key):
        """
        category_detail_view

        method returns the appropriate render
        """

        return render(request, 'base/templates/category_detail.html', context)

class QuestionDetailView(LoginRequiredMixin,PermissionRequiredMixin, generic.DetailView):
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

    '/login/'
        redirect url for login required permission
    """
    from django.shortcuts import get_object_or_404

    model = Question
    template_name = 'question_detail.html'
    login_url = '/login/'
    permission_required = 'canSeeQuestionDetail'
    def get_context_data(self, **kwargs):
        """
        get_context_data

        Method overrides base get_context_view method. This
        method is used to gather objects that are then
        cataloged into a context tuple. Said tuple will be
        sent to HTML templates

        self.object : object
            database object

        this_question : Question
            Question object returned from SQL database

        this_category : Category
            Category object returned from SQL database
        """
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        this_question = Question.objects.get(pk=self.object.pk)
        context['this_question'] = this_question
        my_option_group = this_question.option_group
        context['my_option_group'] = my_option_group
        my_input_type = this_question.input_type_fk
        context['my_input_type'] = my_input_type
        #ObjectDoesNotExist import
        from django.core.exceptions import ObjectDoesNotExist
        #Try catch blocks for queries
        try:
            this_category = Category.objects.get(my_questions__question_fk=this_question)
            context['this_category'] = this_category
        except Survey_Question.DoesNotExist:
            this_category = None
        return context

    def question_detail_view(request, primary_key):
        """
        question_detail_view

        Method, adapted from Django tutorial, will check
        to see if a question exists.

        Question : the obeject we will either retrieve
            or 404 error

        method returns the appropriate render
        """
        Question = get_object_or_404(Question, pk=primary_key)
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

    '/login/'
        redirect url for login required permission

    'canCreateCategory' : permission_required
        Permission requirement to use this view
    """
    model = Category
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
        return reverse('category-detail', kwargs={'surveySlug': self.object.survey_fk.surveySlug,
                                                    'pk': self.object.pk})

    def form_valid(self, form):
        """
        form_valid

        This method is used on HTTP Post,
        we will set our 'Parent Survey' to that
        of the survey passed in with our kwargs
        """

        form.instance.survey_fk = Survey.objects.get(surveySlug=self.kwargs['surveySlug'])
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

    '/login/'
        redirect url for login required permission

    'canUpdateCategory' : permission_required
        Permission requirement to use this view
    """
    model = Category
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
        return reverse('category-detail', kwargs={'surveySlug': self.object.survey_fk.surveySlug,
                                                    'pk': self.object.pk})

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

    '/login/'
        redirect url for login required permission

    'canDeleteCategory' : permission_required
        Permission requirement to use this view
    """
    model = Category
    template_name = 'category_form_confirm_delete.html'
    login_url = '/login/'
    permission_required = 'canDeleteCategory'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('survey-detail', kwargs={'surveySlug': self.object.survey_fk.surveySlug})
    success_url = get_success_url

from .forms import QuestionCreateForm

class QuestionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    QuestionCreate [View]

    Method builds off the generics provided by django to
    offer a user the ability to create a question.

    Question : model
        Question is the model used in this form

    QuestionCreateForm : form_class
        A form that will be used by this view to get information
        from the user

    question_form.html : template_name
        the template we will be using to render
        this view and its contextual data

    '/login/' : login_url
        url link to redirect if one is not logged in

    'canCreateClass' : permission
        the specific permission necessary to use this view

    """
    model = Question
    form_class = QuestionCreateForm
    template_name = 'question_form.html'
    login_url = '/login/'
    permission_required = 'canCreateQuestion'

    def get(self, request, *args, **kwargs):
        """
        get

        Method gets context of this render and returns it to the
        form template to utilize
        """
        context = {'form': QuestionCreateForm()}
        return render(request, 'question_form.html', context)


    def form_valid(self, form):
        """
        form_valid

        Modified from form_valid, this method now not only cleans data
        it also generates the go-between Survey_Question object. Using
        from.instance to get this questions category and survey we then
        save the form and use the instance to create the Survey_Question
        that is the spiritual parent model to Question.

        form.instance.category : Category object
            the parent category for this Question, queried from kwargs

        form.instance.survey : Survey object
            the parent survey for this Question, queried from kwargs

        instance : form
            this is an instance of this form object that is used to grab the
            primary key of Question and pass it to a Survey_Question

        """
        form.instance.category = Category.objects.get(pk=self.kwargs['pk'])
        form.instance.survey = Survey.objects.get(pk=form.instance.category.survey_fk.pk)
        instance = form.save()
        Survey_Question.objects.create(category_fk= form.instance.category,
                                        survey_fk=form.instance.survey,
                                        question_fk=instance)
        print(form.cleaned_data)
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        my_survey_question = Survey_Question.objects.get(question_fk=self.object.pk)
        my_category = Category.objects.get(pk=my_survey_question.category_fk.pk)
        my_survey = Survey.objects.get(pk=my_survey_question.survey_fk.pk)
        return reverse('question-detail', kwargs={'pk': self.object.pk,
                                                    'categoryPk': my_category.pk,
                                                    'surveySlug': my_survey.pk})


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

    '/login/'
        redirect url for login required permission

    'canUpdateQuestion' : permission_required
        Permission requirement to use this view
    """
    model = Question
    template_name = 'question_form.html'
    form_class = QuestionCreateForm
    login_url = '/login/'
    permission_required = 'canUpdateQuestion'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        my_survey_question = Survey_Question.objects.get(question_fk=self.object.pk)
        my_category = Category.objects.get(pk=my_survey_question.category_fk.pk)
        my_survey = Survey.objects.get(pk=my_survey_question.survey_fk.pk)
        return reverse('question-detail', kwargs={'pk': self.object.pk,
                                                    'categoryPk': my_category.pk,
                                                    'surveySlug': my_survey.pk})

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
        my_survey_question = Survey_Question.objects.get(question_fk=self.object.pk)
        my_category = Category.objects.get(pk=my_survey_question.category_fk.pk)
        my_survey = Survey.objects.get(pk=my_survey_question.survey_fk.pk)
        return reverse('survey-detail', kwargs={'surveySlug': my_survey.surveySlug})

from .forms import OptionChoiceForm, OptionGroupForm, OptionGroupChoiceForm


class OptionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    OptionUpdate View

    View for updating option groups

    '/login/'
        redirect url for login required permission

    'canUpdateOption' : permission_required
        Permission requirement to use this view
    """
    model = Option_Group
    fields = ['name_of_group']
    template_name = 'option_form.html'
    login_url = '/login/'
    permission_required = 'canEditOptions'
    context = {
            'Groupform': OptionGroupForm(),
            'Choiceform': OptionChoiceForm()
        }

    def get(self, request, *args, **kwargs):
        """
        get


        Method gets context of this render and returns it to the
        form template to utilize
        """
        context = {
            'Groupform': OptionGroupForm(),
            'Choiceform': OptionChoiceForm()}
        return render(request, 'option_form.html', context)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(OptionUpdateView, self).form_valid(form)

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('option-detail', kwargs={'pk': self.object.pk})

class OptionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Method builds off the generics provided by django to
    offer a user the ability to delete an option group.
    On submission we go back to the option group list page
    On cancel we return to the previous window

    Option_Group : model
        Option_Group is the model used in this form

    option_form_confirm_delete.html : template_name
        The name of the template we want Djagno
        to use when creating this view.

    '/login/'
        redirect url for login required permission

    'canDeleteOption' : permission_required
        Permission requirement to use this view
    """
    model = Option_Group
    template_name = 'option_form_confirm_delete.html'
    login_url = '/login/'
    permission_required = 'canDeleteOptions'

    def get_success_url(self):
        """
        get_success_url

        If the option group is successfully deleted, then the user
        will be returned to the option group list
        """
        return reverse('option-list')
    success_url = get_success_url

class OptionDetailView(LoginRequiredMixin, generic.DetailView):
    """
    OptionListView

    This class lists all currently registered
    Option Groups on the website.

    Parameters
    ----------
    Option_Group : model
        The specific model we're trying to list
    'option_list' : context_object_name
        this is what we will refer to when trying
        to query via HTML
    'option_list.html'
        the name of our html file that contains
        the template we will use
    '/login/'
        redirect url for login required permission
    """
    model = Option_Group
    context_object_name = 'option_detail'
    template_name = 'option_detail.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        """
        get_context_data

        Method overrides base get_context_view method. This
        method is used to gather objects that are then
        cataloged into a context tuple. Said tuple will be
        sent to HTML templates

        self.object : object
            database object

        this_group : Option_Group
            A category object that will be passed to HTML

        myChoices : Queryset
            a queryset of option choices that will be passed to HTML
        """
        context = super(OptionDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        this_group = Option_Group.objects.get(pk=self.object.pk)
        context['option_groups'] = this_group

        from django.core.exceptions import ObjectDoesNotExist

        try:
            myChoices = Option_Choice.objects.filter(option_group_id=this_group)
            context['myChoices'] = myChoices
        except Option_Group.DoesNotExist:
            myChoices = None
        return context

    def category_detail_view(self, request, primary_key):
        """
        category_detail_view

        method returns the appropriate render
        """

        return render(request, 'base/templates/option_detail.html', context)

#Is linked
def OptionListView(request):
    """
    OptionListView

    This class lists all currently registered
    option groups on the website.

    Parameters
    ----------
    Option_Group : model
        The specific model we're trying to list
    'option_list' : context_object_name
        this is what we will refer to when trying
        to query via HTML
    'option_list.html'
        the name of our html file that contains
        the template we will use
    '/login/'
        redirect url for login required permission
    """
    if not request.user.is_authenticated:
         return redirect('/login/')

    context = {'option_list' : Option_Group.objects.all(),
                'option_choices' : Option_Choice.objects.all()}
    return render(request, 'option_list.html', context)

# Is linked to a page
def CreateChoice(request):

    if request.method == "POST":
        form = OptionGroupChoiceForm(request.POST)
        if form.is_valid():
            name_of_group = form.cleaned_data.get('name_of_group')
            option_group = Option_Group.objects.create(
                name_of_group=name_of_group
            )
            option_group.save()

            for (i, text) in form.option_choice():
                Option_Choice.objects.create(
                    option_group=option_group,
                    choice_text=text,
                    weight=int(i)
                )
            print('hello')
            return redirect('option-list')

    return render(request, 'option_form.html', {'Groupform' : OptionGroupChoiceForm()})





class ChoiceUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    CategoryUpdate View

    Method builds off the generics provided by django to
    offer a user the ability to update a category

    Option_Choice : model
        Option_Choice is the model used in this form

    choice_form.html : template_name
        The name of the template we want Djagno
        to use when creating this view.

    '/login/'
        redirect url for login required permission

    'canUpdateOptions' : permission_required
        Permission requirement to use this view
    """
    model = Option_Choice
    template_name = 'choice_update.html'
    fields = ['choice_text',]
    login_url = '/login/'
    permission_required = 'canUpdateOptions'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('option-list')

class ChoiceDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    ChoiceDelete View

    Method builds off the generics provided by django to
    offer a user the ability to delete an option choice.
    On submission we go back to the survey detail page
    On cancel we return to the previous window

    Option_Choice : model
        Category is the model used in this form

    option_choice_form_confirm_delete.html : template_name
        The name of the template we want Djagno
        to use when creating this view.

    '/login/'
        redirect url for login required permission

    'canDeleteOptions' : permission_required
        Permission requirement to use this view
    """
    model = Option_Choice
    template_name = 'choice_delete.html'
    login_url = '/login/'
    permission_required = 'canDeleteOptions'

    def get_success_url(self):
        """
        get_success_url

        takes a self paremeter and uses this to find its slug field(and others)
        to dynamically generate a url to our object
        """
        return reverse('option-list')


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
    """

    generateNewSurvey view

    used for establishing a session to monitor
    what current page we are on, and creates a user_survey object
    for establishing a wether or not the user has taken the survey

    TODO: need to check if user had a survey
    """

    if not request.user.is_authenticated:
        return redirect('/login/')

    survey = Survey.objects.get(surveySlug=surveySlug)
    request.session['surveySlug'] = surveySlug
    request.session['totalPage'] = survey_page_counter(survey)
    request.session['currPage'] = 0

    u_s = User_Survey.objects.create(user_fk=request.user, survey_fk=survey)
    u_s.save()
    request.session['User_Survey_pk'] = u_s.pk
    return redirect(survey.get_take_url())

def welcomeSurvey(request, surveySlug):
    """

    welcomeSurvey view

    used for displaying a welcome page that gives the description
    of the survey before the person starts it

    OPTIONAL TODO: Do we want instructions for a survey to be added?
    TODO: need to check if user had a survey
    """

    if not request.user.is_authenticated:
        return redirect('/login/')

    survey = Survey.objects.get(surveySlug=surveySlug)
    context = {
         'Survey' : survey,
    }
    return render(request, 'welcome_to_survey.html', context)

from .forms import SurveyCategoryForm

def takeSurvey(request, surveySlug, page):
    """
    takeSurvey view

    This view is used for taking the survey and hands off
    each category and each question under those categories.
    this view hands off the category to the SurveyCategoryForm.

    We use the session to keep track of which page were currenlty on
    and incriment based on the page.
    If we have the totalPage eqal to current page the redirect the
    user to the results otherwise handle the post method and save
    the information to a new answer model

    TODO: need to check if user had a survey in User_Survey
    TODO: Save answers of all types rather than just radio
    """

    currPage = request.session.get('currPage', 0)
    totalPage = request.session.get('totalPage', 0)
    survey = Survey.objects.get(surveySlug=request.session.get('surveySlug'))
    list_of_categories = Category.objects.filter(survey_fk=survey)[::1]

    form = SurveyCategoryForm(request.POST, instance=list_of_categories[currPage].pk)
    u_s = User_Survey.objects.get(pk=request.session.get('User_Survey_pk'))
    if form.is_valid():

        for (q, a) in form.category_answers():
            answer = Answer.objects.create(
                user_survey_fk = u_s,
                survey_question_fk = Survey_Question.objects.get(pk=q),
                answer_text = a
            )
            answer.save()

        request.session['currPage'] = currPage + 1
        currPage += 1
    if currPage == totalPage:
            return redirect(u_s.get_result_url())

    form = SurveyCategoryForm(instance=list_of_categories[currPage].pk)

    context = {
        'toc' : list_of_categories[currPage].titleOfCategory,
        'form' : form,
    }
    return render(request, 'take_survey.html', context)

def results(request, surveySlug, pk):
    """
    """
    survey = Survey.objects.get(surveySlug=surveySlug)
    categories = Category.objects.filter(survey_fk=survey)
    u_s = User_Survey.objects.get(pk=pk)
    answers = Answer.objects.filter(user_survey_fk = u_s)
    survey_questions = Survey_Question.objects.filter(survey_fk=survey)
    questions = Question.objects.all()
    true_score = 0
    false_score = 0
    range_average = []
    #Lord help this code :(
    #TODO: LEARN BETTER QUERYING
    #MY EYES!
    #Maybe isolation would help this?
    for answer in answers:
        for survey_question in survey_questions:
            if answer.survey_question_fk == survey_question:
                for question in questions:
                    if survey_question.question_fk == question:
                        if question.input_type_fk.input_type_name == 'range':
                            option_choice = Option_Choice.objects.get(choice_text=answer.answer_text)
                            range_average.append(option_choice.weight + 1)
                        elif question.input_type_fk.input_type_name == 'tf':
                            if answer.answer_text == 'f':
                                false_score += 1
                            else:
                                true_score += 1

    if len(range_average) != 0:
        range_average = sum(range_average) / len(range_average)
    else:
        range_average = 0
    context = {
        'version_number' : survey.version_number,
        'true_score' : true_score,
        'false_score' : false_score,
        'range_average' : range_average,
        'surveySlug': surveySlug,
        'survey_name': survey.titleOfSurvey,
        'categories': categories,
        'answers' : answers,
        'questions' : questions,
        'survey_questions' : survey_questions
    }

    return render(request, 'results.html', context)

