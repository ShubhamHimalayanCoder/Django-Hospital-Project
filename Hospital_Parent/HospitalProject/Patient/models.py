from django.db import models

# Create your models here.

class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True, unique=True)
    patient_full_name = models.CharField(max_length=100)
    patient_father_name = models.CharField(max_length=100)
    patient_age = models.SmallIntegerField()
    patient_gender = models.CharField(max_length=10)
    patient_mobile = models.CharField(max_length=10,unique=True)
    patient_email = models.EmailField(max_length=100,unique=True)
    patient_city = models.CharField(max_length=50)
    patient_symptoms = models.CharField(max_length=1000)
    registeration_time = models.DateField(auto_now_add=True)
    patient_image = models.ImageField(upload_to='patient_image/',null=True) # For uploaded photo


    def __str__(self) -> str:
        return f'Patient ID : {self.patient_id}, Name : {self.patient_full_name}'