from django.shortcuts import render,redirect, HttpResponse
from . import models

# For error handling
from django.db import IntegrityError
from django.db.models import Q

# For excel file
import pandas as pd
from django.conf import settings
import os

# For pagination
from django.core.paginator import Paginator

# For login and signup
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def patient(request,page):
    if request.GET:
        query = request.GET['search']
        patients = models.Patients.objects.filter(Q(patient_full_name__icontains=query)
        | Q(patient_email__icontains=query) | Q(patient_mobile__icontains=query)
        | Q(patient_symptoms__icontains=query)).all()
        data = {
            'patients' : patients
        }
        return render(request,'Patient/patient.html',context=data)

    if request.POST:
        full_name = request.POST['full_name']
        father_name = request.POST['father_name']
        age = request.POST['age']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        email = request.POST['email']
        city = request.POST['city']
        symptoms = request.POST['symptoms']

        if all([full_name,father_name,age,mobile,email,gender,city,symptoms]):
            if request.FILES.get('image'):
                image = request.FILES['image']
                try:
                    patient = models.Patients()
                    patient.patient_full_name = full_name
                    patient.patient_father_name = father_name
                    patient.patient_age = age
                    patient.patient_gender = gender
                    patient.patient_mobile = mobile
                    patient.patient_email = email
                    patient.patient_city = city
                    patient.patient_symptoms = symptoms
                    patient.patient_image = image
                    patient.save()
                    return render(request,'appointment.html',context={'success':'done'})
                except IntegrityError as e:
                    if 'patient_email' in str(e):
                        error = {
                            'error': 'email-error'
                        }
                    elif 'patient_mobile' in str(e):
                        error = {
                            'error' : 'mobile-error'
                        }
                    else:
                        error = {
                            'error' : 'anything else'
                        }
            else:
                error = {
                    'error' : 'empty-image'
                }
        else:
            error = {
                'error':'empty-fields'
            }
        return render(request,'appointment.html',context=error)
            

    # "select * from patients;"
    patients = models.Patients.objects.all()

    paginator = Paginator(patients,4)
    pagination_patients = paginator.page(number=page)

    data = {
        'patients' : pagination_patients
    }
    return render(request,'Patient/patient.html',context=data)
    # cars = ['Ford','BMW','Audi']

def delete_patient(request,id):
    ex_patient = models.Patients.objects.get(patient_id=id)
    ex_patient.patient_image.delete()
    ex_patient.delete()
    return redirect("Patient:patient-page")

def update_patient(request,id):
    if request.POST:
        full_name = request.POST['full_name']
        father_name = request.POST['father_name']
        age = request.POST['age']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        email = request.POST['email']
        city = request.POST['city']
        symptoms = request.POST['symptoms']

        if all([full_name,father_name,age,mobile,email,gender,city,symptoms]):
                try:
                    patient = models.Patients.objects.get(patient_id=id)
                    patient.patient_full_name = full_name
                    patient.patient_father_name = father_name
                    patient.patient_age = age
                    patient.patient_gender = gender
                    patient.patient_mobile = mobile
                    patient.patient_email = email
                    patient.patient_city = city
                    patient.patient_symptoms = symptoms
                    if request.FILES.get('image'):
                        patient.patient_image.delete()
                        patient.patient_image = request.FILES.get('image')
                    patient.save()
                    return render(request,'Patient/update.html',context={'success':'done','patient' : patient})
                except IntegrityError as e:
                    if 'patient_email' in str(e):
                        error = {
                            'error': 'email-error'
                        }
                    elif 'patient_mobile' in str(e):
                        error = {
                            'error' : 'mobile-error'
                        }
                    else:
                        error = {
                            'error' : 'anything else'
                        }
        else:
            error = {
                'error':'empty-fields'
            }
        error['patient'] = patient
        return render(request,'Patient/update.html',context=error)
        
    patient = models.Patients.objects.get(patient_id=id)
    data = {'patient':patient}
    return render(request,'Patient/update.html',context=data)


def filter_patient(request,by):
    if by == 'male':
        patients = models.Patients.objects.filter(patient_gender='male').all()
        data = {
            'patients' : patients
        }
    elif by == 'female':
        patients = models.Patients.objects.filter(patient_gender='female').all()
        data = {
            'patients' : patients
        }
    elif by == 'age-asc':
        patients = models.Patients.objects.order_by('patient_age')
        data = {
            'patients' : patients
        }
    elif by == 'age-desc':
        patients = models.Patients.objects.order_by('-patient_age')
        data = {
            'patients' : patients
        }
    return render(request,'Patient/patient.html',context=data)
    

def convert_to_excel(request):
    patients = models.Patients.objects.all().values('patient_id','patient_full_name','patient_father_name','patient_age','patient_gender','patient_mobile','patient_email','patient_city','patient_symptoms')
    columns = ['ID', 'Name', 'Age', 'Gender', 'Phone', 'Email', 'City', 'Symptoms', 'Registeration Date']
    raw =pd.DataFrame(patients)
    raw.columns = columns
    file_path = os.path.join(settings.MEDIA_ROOT,'patient_excel_file/patients.xlsx')
    raw.to_excel(file_path)
    return redirect('Patient:download-excel')

def download_excel_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'patient_excel_file/patients.xlsx')
    if os.path.exists(file_path):
        with open(file_path,'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="patients.xlsx"'
            return response
    else:
        return HttpResponse('File not found')
    

def signup(request):
    if request.POST:
        full_name = request.POST.get('full_name')
        designation = request.POST.get('designation')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if all([full_name,designation,email,mobile,password,confirm_password]):
            if password == confirm_password:
                encrypt_password = make_password(password)
                try:
                    models.Staff.objects.create(staff_name=full_name,
                                                staff_designation=designation,
                                                staff_email=email,
                                                staff_mobile=mobile,
                                                staff_password=encrypt_password)
                    return render(request, 'Patient/signup.html', context={'success':'done'})
                except IntegrityError as e:
                    if 'staff_email' in str(e):
                        error={
                            'error' : 'email-error'
                        }
                    else:
                        error = {
                            'error' : 'mobile-error'
                        }
            else:
                error = {
                    'error' : 'password-mismatch'
                }
        else:
            error = {
                'error' :'empty-fields'
            }
        return render(request, 'Patient/signup.html', context=error)

    return render(request, 'Patient/signup.html')


def staff_login(request):
    return render(request, 'Patient/login.html')