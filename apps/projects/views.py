from django.views.generic import ListView, DetailView
from .models import Project
from django.utils.safestring import mark_safe
import markdown

import logging
logger = logging.getLogger(__name__)

class ProjectListView(ListView):
	model = Project
	template_name = "projects/list.html"
	context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Convertir el campo readme (Markdown) a HTML
        github_readme_html = None
        if project.readme:
            github_readme_html = markdown.markdown(
                project.readme,
                extensions=[
                    "extra",
                    "codehilite",
                    "toc",
                    "tables",
                    "fenced_code"
                ]
            )
            github_readme_html = mark_safe(github_readme_html)

        context["github_readme_html"] = github_readme_html
        return context