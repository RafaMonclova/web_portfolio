from django import forms
from .models import Post
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Título del Post",
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-700/50 rounded-xl px-4 py-3 text-lg bg-gray-900/60 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 transition-all duration-200',
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
