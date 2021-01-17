"""AppConfig for the survey application

Set survey app related defaults and configs here

"""
from django.apps import AppConfig


class SurveyConfig(AppConfig):
    """Configuration encapsulation class

    Attributes:
    ----------
    name: app name(namespace)
    """
    name = 'survey'
