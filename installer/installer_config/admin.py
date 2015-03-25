from django.contrib import admin
from installer_config.models import EnvironmentProfile
from installer_config.models import UserChoice, Step


# class PackageAdmin(admin.ModelAdmin):
#     model = Package
#     list_display = ('id', 'display_name', 'version', 'website')


# class TerminalPromptAdmin(admin.ModelAdmin):
#     model = TerminalPrompt
#     list_display = ('id', 'display_name', 'install_name', 'description')


class EnvironmentProfileAdmin(admin.ModelAdmin):
    model = EnvironmentProfile
    list_display = ('id', 'user', 'description',)


class ChoiceInline(admin.TabularInline):
    model = Step
    extra = 2


class UserChoiceAdmin(admin.ModelAdmin):
    model = UserChoice
    inlines = [ChoiceInline]
    list_display = ('id', 'description', 'display_order')


class StepAdmin(admin.ModelAdmin):
    model = Step
    list_display = ('id', 'step_type', 'url', 'args', 'dependency', 'user_choice')

# admin.site.register(Package, PackageAdmin)
# admin.site.register(TerminalPrompt, TerminalPromptAdmin)
admin.site.register(UserChoice, UserChoiceAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(EnvironmentProfile, EnvironmentProfileAdmin)
