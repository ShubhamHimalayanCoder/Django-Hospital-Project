# Generated by Django 5.0.6 on 2024-05-22 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0003_patients_patient_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='patient_image',
            field=models.ImageField(null=True, upload_to='patient_image/'),
        ),
    ]