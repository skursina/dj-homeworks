from rest_framework import serializers

from django_testing import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")
    
    def validate_students(self, value):
        max_students = getattr(settings,"MAX_STUDENTS_PER_COURSE", None)

        if max_students and len(value) > max_students :
            raise serializers.ValidationError(f"Максимум {max_students} студентов на курсе.")
        
        return value
