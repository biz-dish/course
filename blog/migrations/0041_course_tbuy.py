# Generated by Django 4.1 on 2022-10-19 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tbuy',
            field=models.BooleanField(null=True),
        ),
    ]