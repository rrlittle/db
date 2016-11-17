from django.contrib import admin
from .models import (Person, Measure, ChoiceGroup, Choice, Question,
					Answer, Survey, SurveyQuestion,
					sourceChoice, sourceColumn, SourceQuestion, SourceScheme,
					kwargs)

#  stuff to define surveys
admin.site.register(Person)
admin.site.register(Measure)
admin.site.register(ChoiceGroup)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Survey)

# stuff to define import sources
admin.site.register(SurveyQuestion)
admin.site.register(sourceChoice)
admin.site.register(sourceColumn)
admin.site.register(SourceQuestion)
admin.site.register(SourceScheme)
admin.site.register(kwargs)
