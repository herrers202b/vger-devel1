from django.shortcuts import render
from .models import Survey, Category, Question, SurveyInstance
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect



@staticmethod
def getNextStage(current_stage, survey):
    n_categories = Category.objects.filter(survey=survey).count()

    if current_stage == n_categories:
        return None
    return n_categories + 1


# Create your views here.
class SurveyTakingView(generic.FormView):
    #TODO: make survey taking template
    template = ''
    survey = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        survey_id = request.session.get("survey_id", None)
        self.survey = Survey.objects.get(id=survey_id)
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.request.session["survey_id"] = form.instance.survey_id
        current_stage = form.cleaned_data.get("stage")
        new_stage = getNextStage(current_stage, self.survey)
        form.instance.stage = new_stage

        if new_stage == None:
            return redirect(reverse('/'))
        return redirect(reverse("survey:survey"))#?
    
    def get_form_class(self):
        stage = self.survey.stage if self.survey else 0
        return super().get_form_class()

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
