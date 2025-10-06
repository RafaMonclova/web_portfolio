from django.shortcuts import render
from .models import About

# Create your views here.

def about_detail(request):
    about = About.objects.first()
    experiences = about.experiences.prefetch_related("tasks").all() if about else []
    educations = about.educations.all() if about else []
    return render(request, "about/detail.html", {
        "about": about,
        "experiences": experiences,
        "educations": educations
    })