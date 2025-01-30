"""Model mappings and registration with admin

Additional Package: nested_admin
nested_admin package allows nesting of inlines i.e., it allows creation
of nested objects in one form with four different classes for model mappings:
1 - NestedModelAdmin
2 - NestedInlineModelAdmin
3 - NestedStackedInline
4 - NestedTabularInline

For further details refer: https://pypi.org/project/django-nested-admin/

Here we map the admin to Survey Model with two levels of nesting on Questions and Choices.
All Nested Objects are collapsed by default in the form by setting classes=['collapse']
"""

from django.contrib import admin
from django.urls import path
import nested_admin
from .models import Survey, Question, Choice, Feedback
from confluent_kafka import Producer, Consumer
import os


class ChoiceInLine(nested_admin.NestedTabularInline):
    """Class to create inline choice nestings for Question objects

    Nested Choices are collapsed by default
    """
    model = Choice
    extra = 2
    classes = ['collapse']


class QuestionInLine(nested_admin.NestedTabularInline):
    """Class to create inline choice nestings for Survey objects

        Nested Questions are collapsed by default
        """
    model = Question
    extra = 1
    classes = ['collapse']
    inlines = [ChoiceInLine]


class SurveyAdmin(nested_admin.NestedModelAdmin):
    """Class to create model admin mapping for Survey objects

        Here the form fields can be specified using fieldsets attribute.
        published_on attribute form for Survey objects are collapsed by default.
        """
    fieldsets = [
        ('Survey Name', {'fields': ['name']}),
        ('When would you like to publish it?', {'fields': ['published_on'], 'classes': ['collapse']})
    ]
    inlines = [QuestionInLine]
    list_filter = ['published_on']
    search_fields = ['name']


class MyAdminSite(admin.AdminSite):
    def all_feedbacks(self, request):
        feedbacks = []
        print("Chucky here! Inside all_feedbacks")
        return {'feedbacks': feedbacks}

    def get_app_list(self, request, **kwargs):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "My Custom App",
                "app_label": "my_test_app",
                # "app_url": "/admin/test_view",
                "models": [
                    {
                        "name": "tcptraceroute",
                        "object_name": "tcptraceroute",
                        "admin_url": "/admin/test_view",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        print("Chucky getting to urls!!!")
        my_urls = [
            path('/admin/', self.all_feedbacks, name="all_feedbacks"),
        ]
        return my_urls + urls


admin_site = MyAdminSite(name="my_admin")
admin.site.register(Feedback, site=admin_site)


# Register Survey objects along with their nestings and fieldssets with admin
# Other entities need not be registered here since they are already bound to Survey object.
# Participant entity will not be used from admin views. Therefore it is not being registered here.
admin.site.register(Survey, SurveyAdmin)
