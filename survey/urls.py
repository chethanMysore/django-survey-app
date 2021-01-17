"""Routing for survey application

This file consists of URL routes for the survey application.
The application is a Single Page Application(SPA) with 5 views.

About:
-----
About page briefly explains the goal and features of the project.

Surveys:
--------
This page lists all the available surveys created by the admin.
Each survey can be interacted with and on click routes to survey details page.

Survey Details:
---------------
This page renders a form with the questionnaire for the survey.
Each question has atleast two choices and are radio inputs.

Survey Submit Success:
----------------------
This is the success landing page for successful submission of the survey.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Default path is /survey/ which invokes index view without any params
    path('', views.index, name="index"),

    # API GET endpoint for returning popular survey among existing surveys.
    # This endpoint can also be used as a web hook in future. Currently it is used within the application.
    path('get_popular_survey/', views.get_popular_survey, name="get_popular_survey"),

    # API GET endpoint for returning survey objects along with corresponding questions and choices.
    # This endpoint can also be used as a web hook in future. Currently it is used within the application.
    path('get_all_surveys/', views.get_all_surveys, name="get_all_surveys"),

    # This is the view hook to submit survey form,
    # update entities based on the submitted form and redirect to success page
    path('submit_survey/', views.submit_survey, name="submit_survey"),

    # This is the generic route for rendering all partial views without params
    # All routes are intercepted by index view middleware and respective partial view will be rendered accordingly
    # Note: This is a work around as at this point I could not find a better solution
    # or documentation to create partial views
    path('<str:partial_view>/', views.index, name="index/partial_view"),

    # This is the generic route for rendering partial views with id parameter
    path('<str:partial_view>/<int:pk>', views.index, name="index/partial_view/id"),
]
