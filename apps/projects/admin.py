from django.contrib import admin
from .models import Project, ProjectImage, Technology, Language


class ProjectImageInline(admin.TabularInline):
	model = ProjectImage
	extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ("title", "type", "framework")
	search_fields = ("title", "framework")
	inlines = [ProjectImageInline]
	filter_horizontal = ('technologies', 'languages')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
	list_display = ('project', 'caption')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
	list_display = ('name',)
