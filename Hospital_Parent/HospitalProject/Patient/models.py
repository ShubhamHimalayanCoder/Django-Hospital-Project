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


    def __str__(self):
        return f'Patient ID : {self.patient_id}, Name : {self.patient_full_name}'
    


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True,unique=True)
    staff_name = models.CharField(max_length=100)
    staff_designation = models.CharField(max_length=20)
    staff_email = models.EmailField(max_length=100, unique=True)
    staff_mobile = models.CharField(max_length=10,unique=True)
    staff_password = models.CharField(max_length=18,editable=False)

    def __str__(self):
        return f'Staff ID : {self.staff_id}, Designation : {self.staff_designation}'