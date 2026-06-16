from django.contrib import admin

from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    search_fields = ('name', 'group', 'teachers__name')
    list_filter = ('group', 'teachers')
    filter_horizontal = ('teachers',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject')
    list_filter = ('subject',)
