"""Python Database API

Django DB Models can be used to create schemas for database entities
which will then be used to create the physical database.

Models:
-------
Survey:
Survey entity encapsulates basic attributes of a survey including
name(survey name) and published_on(date time when the survey is published.
Methods:
    __str__: returns the survey name as metadata reference when objects are accessed.
    was_published_recently: returns True if the survey was published in the last 24h.
                            The callback is also used by the admin for filtering surveys.

Participant:
This entity helps keep track of number of successful survey submits. This entity is used
to identify the popular survey i.e., the survey with most submissions.
The attributes include survey(foreign key referencing Survey) and participation_datetime.
Methods:
    __str__: returns the Participant name as metadata reference when objects are accessed.

Question:
This entity encapsulates a question in the survey with survey(foreign key referencing Survey),
question_text(actual question text) and created_on.
Methods:
    __str__: returns the Question name as metadata reference when objects are accessed.

Choice:
This entity encapsulates a choice attribute in the survey with Question(foreign key referencing Question),
choice_text(actual choice text), votes(to store poll results) and created_on.
Methods:
    __str__: returns the Choice name as metadata reference when objects are accessed.

"""

from django.db import models
from django.utils import timezone
import datetime


class Survey(models.Model):
    """Class to encapsulate Survey entity
    Attributes:
        name: character field with max_length=200
        published_on: datetime field

    """
    name = models.CharField(max_length=200)
    published_on = models.DateTimeField('Published DateTime')

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_on <= now

    was_published_recently.admin_order_field = 'published_on'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Participant(models.Model):
    """Class to encapsulate Participant entity
    Attributes:
        survey: foreign key to Survey
        participation_datetime: datetime field

    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    participation_datetime = models.DateTimeField('Participation DateTime')

    def __str__(self):
        return "Participant "+str(self.participation_datetime)


class Question(models.Model):
    """Class to encapsulate Participant entity
    Attributes:
        survey: foreign key to Survey
        question_text: character field with max_length=200
        created_on: datetime field

    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    created_on = models.DateTimeField('Creation DateTime')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Class to encapsulate Participant entity
    Attributes:
        survey: foreign key to Question
        choice_text: character field with max_length=200
        created_on: datetime field
        votes: number with default 0

    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    created_on = models.DateTimeField('Creation DateTime')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
