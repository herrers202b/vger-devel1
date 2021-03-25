from django.shortcuts import render
from .models import Survey, Category, Question, SurveyInstance
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
from .forms import SurveyCategoryForm





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


def generateNewSurvey(request, pk):
    """
    generateNewSurvey

    
    #TODO: need to check if user had a survey
    #TODO: if survey is already in the survey_instance with user ask if they want to continue the old one
    """
    
    if not request.user.is_authenticated:
        return redirect('/login/')
    new_survey = Survey.objects.get(pk=pk)
    categories = Category.objects.filter(survey=new_survey)
    
    new_survey.pk = None
    new_survey.assigned = True
    new_survey.save()
    for c_item in categories:
        questions = Question.objects.filter(category=c_item)
        c_item.pk = None
        c_item.survey = new_survey
        c_item.save()
        for q_item in questions:
            q_item.pk = None
            q_item.category = c_item
            q_item.save()
        

    survey_instance = SurveyInstance.objects.create(survey=new_survey, user=request.user)
    survey_instance.save()
    return redirect(survey_instance.get_welcome_url())

def welcomeSurvey(request, session_hash):
    request.session['session_hash'] = session_hash
    SI = SurveyInstance.objects.get(session_hash=session_hash)
    context = {
        'Survey' : SI.survey,
        'SI' : SI
    }
    return render(request, 'welcome_to_survey.html', context)
#TODO: Handle return session accessing
def takeSurvey(request, session_hash, page):
    session_category = request.session.get('session_category', None)
    if session_category == None or session_category == []:
        session_category = []
        si = SurveyInstance.objects.get(session_hash=session_hash)
        categories = Category.objects.filter(survey=si.survey)
        for cat in categories:
            session_category.append(cat.titleOfCategory)
        request.session['session_category'] = session_category

    elif len(session_category) != 0:
        if request.method == 'POST':
            form = SurveyCategoryForm(request.POST, instance=session_category[0])
            if form.is_valid():
                si = SurveyInstance.objects.get(session_hash=session_hash)
                category = Category.objects.get(survey=si.survey, titleOfCategory=session_category[0])
                questions = Question.objects.filter(category=category) 

                for (q, a) in form.category_answers():
                    model_question = questions.get(questionText=q)
                    model_question.answer = a
                    model_question.save()

            del session_category[0]

        request.session['session_category'] = session_category
    if len(session_category) == 0:
        #TODO: exit survey
        si = SurveyInstance.objects.get(session_hash=request.session['session_hash'])
        si.survey.finished = True
        si.save()
        return render(request, 'home.html')
        print("TODO")

    #print(request.session['session_category'])
    #TODO: if post save questions
    form = SurveyCategoryForm(instance=session_category[0])

    return render(request, 'take_survey.html', {'toc': session_category[0], 'form' : form})

