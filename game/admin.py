from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Submission, Team, Problem, Category, RewardCode, AdminSetting


class TeamAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'score', 'team_members'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'score', 'team_members')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Team, TeamAdmin)
admin.site.register(Submission)
admin.site.register(Problem)
admin.site.register(Category)
admin.site.register(RewardCode)
admin.site.register(AdminSetting)
