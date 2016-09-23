from django.contrib import admin
from .models import (Person,Measure,Choice_Group,
					Choice,Question,
					# Question_Choice,
					Answer,
					Survey, Survey_Question)


admin.site.register(Person)
admin.site.register(Measure)
admin.site.register(Choice_Group)
admin.site.register(Choice)
admin.site.register(Question)
# admin.site.register(Question_Choice)
admin.site.register(Answer)
admin.site.register(Survey)
admin.site.register(Survey_Question)