from django.contrib import admin
from .models import User, Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "description")
admin.site.register(User)
admin.site.register(Task, TaskAdmin)