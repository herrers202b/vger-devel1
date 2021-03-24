from django.shortcuts import render
#Form imports
from base.forms import SurveyModelFrom
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
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
    #We can create our own template name as needed
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
    """
    from django.shortcuts import get_object_or_404

    model = Survey
    context_object_name = 'survey_detail'
    template_name = 'survey_detail.html' 

    def survey_detail_view(request, primary_key):
        """
        survey_detail_view

        Method, adapted from Django tutorial, will check
        to see if a survey exists.

        Survey : the obeject we will either retrieve 
            or 404 error
        
        method returns the appropriate render
        """
        Survey = get_object_or_404(Survey, pk=primary_key) 
        return render(request, 'base/templates/survey_detail.html', context={'survey': survey})

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
    """
    model = Survey
    fields = ['titleOfSurvey', 'directions']
    template_name = 'survey_form.html' 

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
    """
    
    model = Survey
    fields = ['titleOfSurvey', 'directions']
    template_name = 'survey_form.html' 

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
    
    """
    model = Survey
    template_name = 'survey_form_confirm_delete.html' 
    success_url = reverse_lazy('survey')



"""
def take_survey(request, pk):
    #View function for taking a survey
    Survey = get_object_or_404(Survey, pk=pk)

    #If this is a POST request then process the From data
    if request.method == 'POST':

        #Create a form instance and populate it with data from the request
        form = SurveyModelFrom(request.POST)
        #Check if the form is valid:
        if form.is_valid():
            #Process data 
            #do nothing for now
            #Redirect to new url -> results
            return HttpResponseRedirect(reverse('results'))
    #If this is a GET(or any other method) create the default form
    #else:
        #Do nothing here
    return render(request, 'take_survey.html', context)
    """
