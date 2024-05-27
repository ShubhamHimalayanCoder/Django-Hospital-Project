from django.shortcuts import render,redirect, HttpResponse
from . import models
# For error handling
from django.db import IntegrityError
from django.db.models import Q

# Create your views here.
def patient(request):
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
        # image = request.FILES.get('image')

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

    data = {
        'patients' : patients
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
        
    patient = models.Patients.objects.get(patient_id = id)
    return render(request,'Patient/update.html',context={'patient':patient})

