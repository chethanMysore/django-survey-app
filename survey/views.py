"""Create Views for the application

Here you can create views for the survey application.
Each view will be either mapped directly to a URL in the routing
or will be used to render partial views using inclusion_tags.

index:
------
This is the default view for the start site of the application.
Also, this is a middleware for routing requests to partial views.
all_partial_views: is a list of partial views that are registered with index.
Default partial view is 'about'.

all_surveys:
------------
This is the partial view rendering list of surveys created by the admin.
Context object is currently not being used.
However, it is a required param for invoking the view from inclusion template tag.

about:
------
This is the partial view for rendering about page. The view only displays static content.

survey_details:
---------------
This is the partial view for the survey form. It accepts survey id as querystring parameter.
It provides survey details for the survey id provided for the html template.

submit_success:
---------------
This is the partial view for displaying submit success message.

submit_survey:
--------------
This is the hook for form submit which gets the voted choices.
From this it increments the votes of respective choices.
Also, it creates a participant instance tracking the survey participation
and the datetime at which the survey was taken.

get_popular_survey:
-------------------
This is the API GET endpoint for returning popular survey among existing surveys.
This endpoint can also be used as a web hook in future. Currently it is used within the application.

get_all_surveys:
----------------
API GET endpoint for returning survey objects along with corresponding questions and choices.
This endpoint can also be used as a web hook in future. Currently it is used within the application.

"""

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.template.loader_tags import register
from django.views.decorators.http import require_http_methods
from .models import Survey, Question, Choice, Participant
from django.utils import timezone
from django.core import serializers
import operator

all_partial_views = ['about', 'all_surveys', 'survey_details', 'submit_success']


@require_http_methods(["GET"])
def index(request, partial_view=None, pk=None):
    if partial_view is None:
        partial_view = 'about'
        return render(request, 'survey/index.html', {"partial_view": partial_view, "pk": pk})
    elif all_partial_views.count(partial_view) == 0:
        raise Http404('Partial View not found!')
    elif partial_view == "survey_details" and pk is None:
        raise Http404('Invalid Address! Page Not Found')
    else:
        return render(request, 'survey/index.html', {"partial_view": partial_view, "pk": pk})


@register.inclusion_tag('survey/surveys.html', takes_context=True)
def all_surveys(context):
    surveys = Survey.objects.all()
    return {'surveys': surveys}


@register.inclusion_tag('survey/about.html', takes_context=True)
def about(context):
    return {}


@register.inclusion_tag('survey/survey_details.html', takes_context=True)
def survey_details(context, survey_id):
    survey = Survey.objects.get(id=survey_id)
    return {'survey': survey}


@register.inclusion_tag('survey/submit_success.html', takes_context=True)
def submit_success(context):
    return {}


@require_http_methods(["POST"])
def submit_survey(request):
    form_data = request.POST.copy()
    # Example: {'csrfmiddlewaretoken': ['idT13LGpggg78Yr0rU3vSkT1PQxnM9hT7z97FvuZEBb
    # IU2acygAUr2W3FE9SCGbk'], '1': ['choice/3'], '2': ['choice/5']}
    form_items = list(form_data.items())
    print("form_items", form_items)
    form_items.pop(0)  # the first element is the csrf token. Therefore omit it.
    survey = None
    for item in form_items:
        # Here in 'choice/3', '3' is '<choice_id>'.
        choice_str, choice_id = item
        choice_id = int(choice_id.split('/')[1])
        choice = Choice.objects.get(id=choice_id)
        if survey is None:
            survey = choice.question.survey
        choice.votes = choice.votes + 1
        choice.save()
    if survey is not None:
        participant = Participant(survey=survey, participation_datetime=timezone.now())
        participant.save()
    return redirect('/survey/submit_success/')


@require_http_methods(["GET"])
def get_popular_survey(request):
    popular_survey_id = None
    popular_survey = None
    surveys = Survey.objects.all()
    survey_participants_dict = {}
    for survey in surveys:
        num_participants = Participant.objects.filter(survey=survey).count()
        survey_participants_dict[survey.id] = num_participants
    if len(survey_participants_dict) > 0:
        popular_survey_id = max(survey_participants_dict.items(), key=operator.itemgetter(1))[0]
    if popular_survey_id is not None:
        popular_survey = serializers.serialize("json", surveys.filter(id=popular_survey_id))
    return JsonResponse(popular_survey, safe=False)


@require_http_methods(["GET"])
def get_all_surveys(request):
    surveys = Survey.objects.all()
    questions = Question.objects.all()
    choices = Choice.objects.all()

    return JsonResponse({"surveys": serializers.serialize("json", surveys),
                         "questions": serializers.serialize("json", questions),
                         "choices": serializers.serialize("json", choices)})
