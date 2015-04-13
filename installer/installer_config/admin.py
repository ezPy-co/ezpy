from django.contrib import admin
from installer_config.models import EnvironmentProfile
from installer_config.models import UserChoice, Step


class EnvironmentProfileAdmin(admin.ModelAdmin):
    model = EnvironmentProfile
    list_display = ('id', 'user', 'description',)


class ChoiceInline(admin.TabularInline):
    model = Step
    extra = 2


class UserChoiceAdmin(admin.ModelAdmin):
    model = UserChoice
    inlines = [ChoiceInline]
    list_display = ('name', 'description', 'category', 'priority')


admin.site.register(UserChoice, UserChoiceAdmin)
admin.site.register(EnvironmentProfile, EnvironmentProfileAdmin)
