from django import forms
from tasks.models import Task


class FormularioTask(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['title', 'description', 'important']
		labels = {'title': 'Título', 'description': 'Descripción', 'important': 'importante'}

		widgets= {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la Tarea'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la Tarea'}),
		}
