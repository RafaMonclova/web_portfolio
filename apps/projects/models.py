
from django.db import models

class Project(models.Model):
	TYPE_CHOICES = [
		("frontend", "Frontend"),
		("backend", "Backend"),
		("fullstack", "Fullstack"),
	]

	title = models.CharField(max_length=200)
	description = models.TextField()
	# Replaced comma-separated languages field with a ManyToMany to Language
	languages = models.ManyToManyField('Language', blank=True, related_name='projects')
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	github_url = models.URLField()
	readme = models.TextField(blank=True, null=True, help_text="Contenido del README en formato Markdown")
	cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
	technologies = models.ManyToManyField('Technology', blank=True, related_name='projects')

	def __str__(self):
		return self.title

	def get_languages_list(self):
		return [lang.name for lang in self.languages.all()]


class Language(models.Model):
	name = models.CharField(max_length=100, unique=True)
	icon = models.CharField(max_length=200, blank=True, null=True, help_text='Opcional: clase de icono o URL')

	def __str__(self):
		return self.name

	def get_technologies_list(self):
		return [tech.name for tech in self.technologies.all()]


class Technology(models.Model):
	name = models.CharField(max_length=100, unique=True)
	icon = models.CharField(max_length=200, blank=True, null=True, help_text='Opcional: clase de icono o URL')

	def __str__(self):
		return self.name


class ProjectImage(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='projects/gallery/')
	caption = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return f"{self.project.title} - {self.caption or 'image'}"
