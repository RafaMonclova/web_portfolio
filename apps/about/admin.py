from django.contrib import admin
from .models import About, Experience, Education, Task
from .models import Language, Framework, Skill


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1

class FrameworkInline(admin.TabularInline):
    model = Framework
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 1
    show_change_link = True


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "start_date", "end_date")
    inlines = [TaskInline]


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "email")
    inlines = [ExperienceInline, EducationInline, LanguageInline, FrameworkInline, SkillInline]
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "about")

@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ("name", "about")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "about")
