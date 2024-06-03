from django.shortcuts import render,HttpResponse

def home(request):
    return render(request,'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def career(request):
    return render(request, 'career.html')

def faq(request):
    return render(request, 'faq.html')

def appointment(request):
    return render(request, 'appointment.html')

def contact(request):
    return render(request, 'contact.html')

def terms_and_conditions(request):
    return render(request, 't&c.html')

def calling_back(request):
    return render(request, 'callback-dialog.html')
