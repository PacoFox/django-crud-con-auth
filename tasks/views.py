from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils import timezone

from tasks.forms import FormularioTask
from tasks.models import Task


def home(request):
	return render(request, 'home.html')

def signup(request):
	if request.method == 'GET':
		return render(request, 'signup.html', {
			'form': UserCreationForm
		})
	else:
		# Las variables POST: password1, password2, username, vienen del formulario automáticamente creado por Django
		# mediante UserCreationForm.
		if request.POST['password1'] == request.POST['password2']:
			try:
				user= User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])   # Se crea un obj User
				user.save()     # Se guarda el usuario en la BD
				login(request, user)    # login es un método de Django. Sirve para guardar el Usuario en la Sesión(virtual) actual.
				return redirect('tasks')
			except IntegrityError:     # Este error generalmente es causado por tratar de guardar un usuario YA existente.
				return render(request, 'signup.html', {
					'form': UserCreationForm,
					'error': 'El Nombre de Usuario YA existe'
				})
		return render(request, 'signup.html', {
			'form': UserCreationForm,
			'error': 'Las Contraseñas no concuerdan'
		})

def signin(request):
	if request.method == 'GET':     # Si va a desplegar la pág de Registrarse...
		return render(request, 'signin.html', {'form': AuthenticationForm})
	else:                           # Si va a procesar los datos capturados en la pág de Registrarse...
		user= authenticate(request, username= request.POST['username'], password= request.POST['password']) # func. propia de Django
		if user is None:    # Si no lo pudo autenticar...
			return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Usuario o Contraseña incorrecta'})
		else:               # Si el Usuario fue correctamente autenticado...
			login(request, user)    # Se guardan los datos del usuario en la Sesión de Django.
			return redirect('tasks')# y se redirige a la pág. Tareas.

@login_required
def tasks(request):
	tareas= Task.objects.filter(user=request.user, datecompleted__isnull=True )
	return render(request, 'tasks.html', {'tasks': tareas, 'tipo_despliegue': 'P'})   # P)endientes

@login_required
def tasks_completed(request):
	tareas= Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
	return render(request, 'tasks.html', {'tasks': tareas, 'tipo_despliegue': 'C'})   # C)ompletadas

@login_required
def task_detail(request, id_task):
	if request.method == 'GET':     # Si se va a desplegar el formulario...
		tarea = get_object_or_404(Task, pk=id_task, user=request.user)
		formulario= FormularioTask(instance=tarea)
		return render(request, 'task_details.html', {'task': tarea, 'form': formulario})
	else:                           # si es POST para procesar el formulario...
		try:
			tarea = get_object_or_404(Task, pk=id_task)
			formulario= FormularioTask(request.POST, instance=tarea)
			formulario.save()
			return redirect('tasks')
		except ValueError:
			return render(request, 'task_details.html', {'task': tarea, 'form': formulario,
			                                             'error': 'Error al Actualizar la Tarea'})

@login_required
def complete_task(request, id_task):
	tarea= get_object_or_404(Task, pk=id_task, user=request.user)
	if request.method == 'POST':
		tarea.datecompleted= timezone.now()
		tarea.save()
		return redirect('tasks')

@login_required
def delete_task(request, id_task):
	tarea= get_object_or_404(Task, pk=id_task, user=request.user)
	if request.method == 'POST':
		tarea.delete()
		return redirect('tasks')

@login_required
def create_task(request):
	if request.method == 'GET':
		return render(request, 'create_task.html', {'form': FormularioTask})
	else:
		try:
			form= FormularioTask(request.POST)
			new_task = form.save(commit=False)
			new_task.user= request.user
			new_task.save()
			return redirect('tasks')
		except ValueError:
			return render(request, 'create_task.html', {'form': FormularioTask, 'error': 'Proporciona datos válidos por favor.'})


def cerrar_sesión(request):
	logout(request)
	return redirect('home')
