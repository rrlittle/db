from django.contrib import admin
from .models import (Person,Measure,Choice_Group, Choice, Question,
					Answer,Survey, Survey_Question,
					sourceChoices, sourceColumn, SourceQuestion, SourceScheme)

#  stuff to define surveys
admin.site.register(Person)
admin.site.register(Measure)
admin.site.register(Choice_Group)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Survey)

# stuff to define import sources
admin.site.register(Survey_Question)
admin.site.register(sourceChoices)
admin.site.register(sourceColumn)
admin.site.register(SourceQuestion)
admin.site.register(SourceScheme)
