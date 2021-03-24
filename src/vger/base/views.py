from django.shortcuts import render
from .models import Survey, Category, Question, SurveyInstance
from django.views import generic


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

def home(request):
    return render(request, 'home.html')

def results(request):
    """
    results

    num_instances : the object will return the number of 
        times user has taken survey 
    """
    num_instances = SurveyInstance.objects.all().count()
    instance_hash = SurveyInstance.hash()

    context = {
        'num_instances': num_instances,
        'instance_hash': instance_hash,
    }
    return render(request, 'results.html', context=context)