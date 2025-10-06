from django.db import models

class Language(models.Model):
    about = models.ForeignKey('About', on_delete=models.CASCADE, related_name="languages")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Framework(models.Model):
    about = models.ForeignKey('About', on_delete=models.CASCADE, related_name="frameworks")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skill(models.Model):
    about = models.ForeignKey('About', on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class About(models.Model):
    full_name = models.CharField(max_length=120)
    title = models.CharField(max_length=120, help_text="Full Stack Developer")
    description = models.TextField(help_text="A description about you")
    photo = models.ImageField(upload_to="about/", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.full_name


class Experience(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.position} en {self.company}"

class Task(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="tasks")
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Education(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name="educations")
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"
