# Generated by Django 4.0.3 on 2022-05-09 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectC', '0002_attendance_status_alter_attendance_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='teacher_taking', to='projectC.teacher'),
        ),
    ]