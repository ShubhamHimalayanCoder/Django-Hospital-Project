from django.urls import path
from . import views

app_name = 'Patient'

urlpatterns = [
    path('<int:page>/',views.patient, name='patient-page'),
    path('delete/<int:id>', views.delete_patient, name='delete-card'),
    path('update/<int:id>', views.update_patient, name='update'),
    path('filter/<slug:by>', views.filter_patient, name='filter-patient'),
    path('export-to-excel/', views.convert_to_excel, name='to-excel'),
    path('download-excel-file/', views.download_excel_file, name='download-excel'),
    path('signup/', views.signup , name='signup'),
    path('login/', views.staff_login , name='login'),
]