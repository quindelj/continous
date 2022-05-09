# Generated by Django 4.0.3 on 2022-05-09 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectC', '0004_behavior_incident_date_behavior_sign_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='behavior',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_behavior', to='projectC.student'),
        ),
        migrations.AlterField(
            model_name='behavior',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_teacher', to='projectC.teacher'),
        ),
    ]
