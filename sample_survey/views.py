from .templatetags.feedback_tags import all_feedbacks
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers


@require_http_methods(["GET"])
def get_new_feedbacks(request):
    feedbacks = {}
    try:
        feedbacks = all_feedbacks()
        # feedbacks = serializers.serialize('json', feedbacks)
    except Exception as feedbacks_fetch_error:
        print(f'Error Fetching Feedbacks - {feedbacks_fetch_error}')

    return JsonResponse({"feedbacks": feedbacks})
