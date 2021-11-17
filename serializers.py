from rest_framework import serializers
from .models import student_details,student_marks


class studentserializer(serializers.ModelSerializer):
	class Meta:
		model=student_details
		fields='__all__'


class student_mark_serializer(serializers.ModelSerializer):
	class Meta:
		model=student_marks
		fields="__all__"