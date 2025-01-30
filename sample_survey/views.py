# from .models import Survey, Question, Choice, Participant, Feedback
# from .utils import Logger


# @register.inclusion_tag('admin/index.html', takes_context=True)
# @require_http_methods(["GET"])
# async def all_feedbacks(request):
#     feedbacks = []
#     print("Chucky here! Inside all_feedbacks")
#     feedbacks_cl = FeedbacksCluster(topic="feedback")
#     # try:
#     #     feedbacks = await sync_to_async(feedbacks_cl.consume())
#     #     # async with FeedbacksCluster(topic="feedback") as feedbacks_cl:
#     #     #     feedback = await feedbacks_cl.consume()
#     #     #     feedbacks.append(feedback)
#     # except Exception as consume_error:
#     #     print(f'Feedback Consumption Error - {consume_error}')
#     # # config = read_config()
#     # # topic = 'feedback'
#     # # feedbacks = consume(topic, config)
#     # # feedbacks = [(1, "Sample Feedback 1"), (2, "Sample Feedback 2")]
#     # survey_feedbacks = [(1, "25-01-2025", "Sample Message 1"), (2, "24-01-2025", "Sample Message 2")]
#     # # for feedback in survey_feedbacks:
#     # #     typ, created_on, msg = feedback
#     # #     feedbacks.append({'typ': typ, 'created_on': created_on, 'msg': msg})
#     # feedbacks = survey_feedbacks
#     # request.session['feedbacks'] = 'feedbacks'
#     # print(feedbacks)
#     # messages.add_message(request, messages.INFO, feedbacks, extra_tags='feedback')
#     # surveys = Survey.objects.all()
#     # return HttpResponse(f'feedbacks: {feedbacks}')
#     return render('admin/index.html', {'feedbacks': await sync_to_async(feedbacks_cl.consume())})
#     # return redirect('/admin/')
