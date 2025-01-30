from django.apps import AppConfig
from django.core.signals import request_finished
from .Kafka.FeedbacksCluster import FeedbacksCluster


class SampleSurveyConfig(AppConfig):
    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals

        # Explicitly connect a signal handler.
        request_finished.connect(signals.my_callback)
