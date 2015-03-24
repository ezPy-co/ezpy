from django.contrib import admin
from installer_config.models import Package, TerminalPrompt, EnvironmentProfile


class PackageAdmin(admin.ModelAdmin):
    model = Package
    list_display = ('id', 'display_name', 'version', 'website')


class TerminalPromptAdmin(admin.ModelAdmin):
    model = TerminalPrompt
    list_display = ('id', 'display_name', 'install_name', 'description')


class EnvironmentProfileAdmin(admin.ModelAdmin):
    model = EnvironmentProfile
    list_display = ('id', 'user', 'description',)


admin.site.register(Package, PackageAdmin)
admin.site.register(TerminalPrompt, TerminalPromptAdmin)
admin.site.register(EnvironmentProfile, EnvironmentProfileAdmin)
