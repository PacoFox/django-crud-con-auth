from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)


# Register your models here.
from tasks.models import Task

# Para el Admin, se registra la clase Task, configurándola con los parámetros de la clase TaskAdmin.
admin.site.register(Task, TaskAdmin)
