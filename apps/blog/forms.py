from django import forms
from .models import Post
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Título del Post",
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-700 rounded-lg p-3 text-lg bg-gray-800 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Escribe el título aquí...'
        })
    )

    content = forms.CharField(
        label="Contenido del Post",
        widget=TinyMCE(attrs={'cols': 80, 'rows': 20})
    )

    class Meta:
        model = Post
        fields = ['title', 'content']
