from django.contrib import admin

from .models import Submission, Team, Problem, Category

admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(Problem)
admin.site.register(Category)
