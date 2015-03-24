from django.contrib import admin
from installer_config.models import Package, TerminalPrompt, EnvironmentProfile
from installer_config.models import UserChoice, Step


class PackageAdmin(admin.ModelAdmin):
    model = Package
    list_display = ('id', 'display_name', 'version', 'website')


class TerminalPromptAdmin(admin.ModelAdmin):
    model = TerminalPrompt
    list_display = ('id', 'display_name', 'install_name', 'description')


class EnvironmentProfileAdmin(admin.ModelAdmin):
    model = EnvironmentProfile
    list_display = ('id', 'user', 'description',)


class UserChoiceAdmin(admin.ModelAdmin):
    model = UserChoice
    list_display = ('id', 'description')


class StepAdmin(admin.ModelAdmin):
    model = Step
    list_display = ('step_type', 'url', 'args', 'dependency', 'user_choice')

admin.site.register(Package, PackageAdmin)
admin.site.register(TerminalPrompt, TerminalPromptAdmin)
admin.site.register(UserChoice, UserChoiceAdmin)
admin.site.register(Step, StepAdmin)
