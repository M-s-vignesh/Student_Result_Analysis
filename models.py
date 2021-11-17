from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class student_details(models.Model):
	name=models.CharField(max_length=200)
	roll_number=models.IntegerField(unique=True)
	date_of_birth=models.DateField()

class student_marks(models.Model):
	marks=models.IntegerField(default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
     )