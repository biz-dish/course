# Generated by Django 4.1 on 2022-10-19 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_course_tbuy'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='concession',
            field=models.IntegerField(default=0),
        ),
    ]