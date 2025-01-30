"""AppConfig for the survey application

Set survey app related defaults and configs here

"""
from django.apps import AppConfig
from django.core.signals import request_finished


class SurveyConfig(AppConfig):
    """Configuration encapsulation class

    Attributes:
    ----------
    name: app name(namespace)
    """
    name = 'survey'
