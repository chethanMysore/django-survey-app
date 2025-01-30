from django import template
from django.core import serializers
import ast
from ..configs.utils import FeedbackType
from ..Kafka.FeedbacksCluster import FeedbacksCluster
from asgiref.sync import sync_to_async
import asyncio

register = template.Library()


@register.simple_tag
def get_feedback(messages):
    feedbacks = None, None
    if messages:
        feedbacks = [feedback.message for feedback in messages if feedback.extra_tags == 'feedback']
        if feedbacks:
            feedbacks = ast.literal_eval(feedbacks[0])
            print(feedbacks)
    return feedbacks


@register.simple_tag
def get_feedback_type(typ):
    feedback_type = None
    try:
        if typ:
            typ = ast.literal_eval(typ)
            feedback_type = FeedbackType(typ).name
    except Exception as e:
        print(f'Could not find the type of feedback!! {e}')
    return feedback_type


@register.simple_tag
def all_feedbacks():
    feedbacks = []
    print("Chucky here! Inside all_feedbacks")
    feedbacks_cl = FeedbacksCluster(topic="feedback")
    try:
        feedback = "Fetching Messages..."
        while feedback is not None:
            feedback = feedbacks_cl.consume_feedbacks()
            if feedback:
                feedbacks.append(feedback)
        # async with FeedbacksCluster(topic="feedback") as feedbacks_cl:
        #     feedback = await feedbacks_cl.consume()
        #     feedbacks.append(feedback)
    except Exception as consume_error:
        print(f'Feedback Consumption Error - {consume_error}')
    finally:
        print("Closing consumer")
        feedbacks_cl.close()
    # # config = read_config()
    # # topic = 'feedback'
    # # feedbacks = consume(topic, config)
    # # feedbacks = [(1, "Sample Feedback 1"), (2, "Sample Feedback 2")]
    # survey_feedbacks = [(1, "25-01-2025", "Sample Message 1"), (2, "24-01-2025", "Sample Message 2")]
    # # for feedback in survey_feedbacks:
    # #     typ, created_on, msg = feedback
    # #     feedbacks.append({'typ': typ, 'created_on': created_on, 'msg': msg})
    # feedbacks = survey_feedbacks
    # request.session['feedbacks'] = 'feedbacks'
    # print(feedbacks)
    # messages.add_message(request, messages.INFO, feedbacks, extra_tags='feedback')
    # surveys = Survey.objects.all()
    # return HttpResponse(f'feedbacks: {feedbacks}')
    return feedbacks
