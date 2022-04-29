# Generated by Django 4.0.3 on 2022-04-29 11:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectC', '0005_course_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='course_student', to=settings.AUTH_USER_MODEL),
        ),
    ]
