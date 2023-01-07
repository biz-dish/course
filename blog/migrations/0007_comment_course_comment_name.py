# Generated by Django 4.1 on 2022-09-04 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.course'),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Name'),
        ),
    ]